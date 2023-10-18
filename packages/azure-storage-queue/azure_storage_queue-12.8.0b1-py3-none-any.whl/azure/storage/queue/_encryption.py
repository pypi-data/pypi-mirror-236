# pylint: disable=too-many-lines
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import math
import sys
import warnings
from collections import OrderedDict
from io import BytesIO
from json import (
    dumps,
    loads,
)
from typing import Any, BinaryIO, Dict, Optional, Tuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.padding import PKCS7

from azure.core.exceptions import HttpResponseError
from azure.core.utils import CaseInsensitiveDict

from ._version import VERSION
from ._shared import encode_base64, decode_base64_to_bytes


_ENCRYPTION_PROTOCOL_V1 = '1.0'
_ENCRYPTION_PROTOCOL_V2 = '2.0'
_GCM_REGION_DATA_LENGTH = 4 * 1024 * 1024
_GCM_NONCE_LENGTH = 12
_GCM_TAG_LENGTH = 16

_ERROR_OBJECT_INVALID = \
    '{0} does not define a complete interface. Value of {1} is either missing or invalid.'


def _validate_not_none(param_name, param):
    if param is None:
        raise ValueError(f'{param_name} should not be None.')


def _validate_key_encryption_key_wrap(kek):
    # Note that None is not callable and so will fail the second clause of each check.
    if not hasattr(kek, 'wrap_key') or not callable(kek.wrap_key):
        raise AttributeError(_ERROR_OBJECT_INVALID.format('key encryption key', 'wrap_key'))
    if not hasattr(kek, 'get_kid') or not callable(kek.get_kid):
        raise AttributeError(_ERROR_OBJECT_INVALID.format('key encryption key', 'get_kid'))
    if not hasattr(kek, 'get_key_wrap_algorithm') or not callable(kek.get_key_wrap_algorithm):
        raise AttributeError(_ERROR_OBJECT_INVALID.format('key encryption key', 'get_key_wrap_algorithm'))


class StorageEncryptionMixin(object):
    def _configure_encryption(self, kwargs):
        self.require_encryption = kwargs.get("require_encryption", False)
        self.encryption_version = kwargs.get("encryption_version", "1.0")
        self.key_encryption_key = kwargs.get("key_encryption_key")
        self.key_resolver_function = kwargs.get("key_resolver_function")
        if self.key_encryption_key and self.encryption_version == '1.0':
            warnings.warn("This client has been configured to use encryption with version 1.0. " +
                          "Version 1.0 is deprecated and no longer considered secure. It is highly " +
                          "recommended that you switch to using version 2.0. The version can be " +
                          "specified using the 'encryption_version' keyword.")


class _EncryptionAlgorithm(object):
    """
    Specifies which client encryption algorithm is used.
    """
    AES_CBC_256 = 'AES_CBC_256'
    AES_GCM_256 = 'AES_GCM_256'


class _WrappedContentKey:
    """
    Represents the envelope key details stored on the service.

    :param str algorithm:
        The algorithm used for wrapping.
    :param bytes encrypted_key:
        The encrypted content-encryption-key.
    :param str key_id:
        The key-encryption-key identifier string.
    """
    def __init__(self, algorithm, encrypted_key, key_id):
        _validate_not_none('algorithm', algorithm)
        _validate_not_none('encrypted_key', encrypted_key)
        _validate_not_none('key_id', key_id)

        self.algorithm = algorithm
        self.encrypted_key = encrypted_key
        self.key_id = key_id


class _EncryptedRegionInfo:
    """
    Represents the length of encryption elements.
    This is only used for Encryption V2.

    :param int data_length:
        The length of the encryption region data (not including nonce + tag).
    :param str nonce_length:
        The length of nonce used when encrypting.
    :param int tag_length:
        The length of the encryption tag.
    """

    def __init__(self, data_length, nonce_length, tag_length):
        _validate_not_none('data_length', data_length)
        _validate_not_none('nonce_length', nonce_length)
        _validate_not_none('tag_length', tag_length)

        self.data_length = data_length
        self.nonce_length = nonce_length
        self.tag_length = tag_length


class _EncryptionAgent:
    """
    Represents the encryption agent stored on the service.
    It consists of the encryption protocol version and encryption algorithm used.

    :param _EncryptionAlgorithm encryption_algorithm:
        The algorithm used for encrypting the message contents.
    :param str protocol:
        The protocol version used for encryption.
    """

    def __init__(self, encryption_algorithm, protocol):
        _validate_not_none('encryption_algorithm', encryption_algorithm)
        _validate_not_none('protocol', protocol)

        self.encryption_algorithm = str(encryption_algorithm)
        self.protocol = protocol


class _EncryptionData:
    """
    Represents the encryption data that is stored on the service.

    :param Optional[bytes] content_encryption_IV:
        The content encryption initialization vector.
        Required for AES-CBC (V1).
    :param Optional[_EncryptedRegionInfo] encrypted_region_info:
        The info about the authenticated block sizes.
        Required for AES-GCM (V2).
    :param _EncryptionAgent encryption_agent:
        The encryption agent.
    :param _WrappedContentKey wrapped_content_key:
        An object that stores the wrapping algorithm, the key identifier,
        and the encrypted key bytes.
    :param dict key_wrapping_metadata:
        A dict containing metadata related to the key wrapping.
    """

    def __init__(
        self,
        content_encryption_IV,
        encrypted_region_info,
        encryption_agent,
        wrapped_content_key,
        key_wrapping_metadata
    ):
        _validate_not_none('encryption_agent', encryption_agent)
        _validate_not_none('wrapped_content_key', wrapped_content_key)

        # Validate we have the right matching optional parameter for the specified algorithm
        if encryption_agent.encryption_algorithm == _EncryptionAlgorithm.AES_CBC_256:
            _validate_not_none('content_encryption_IV', content_encryption_IV)
        elif encryption_agent.encryption_algorithm == _EncryptionAlgorithm.AES_GCM_256:
            _validate_not_none('encrypted_region_info', encrypted_region_info)
        else:
            raise ValueError("Invalid encryption algorithm.")

        self.content_encryption_IV = content_encryption_IV
        self.encrypted_region_info = encrypted_region_info
        self.encryption_agent = encryption_agent
        self.wrapped_content_key = wrapped_content_key
        self.key_wrapping_metadata = key_wrapping_metadata


class GCMBlobEncryptionStream:
    """
    A stream that performs AES-GCM encryption on the given data as
    it's streamed. Data is read and encrypted in regions. The stream
    will use the same encryption key and will generate a guaranteed unique
    nonce for each encryption region.

    :param bytes content_encryption_key: The encryption key to use.
    :param BinaryIO data_stream: The data stream to read data from.
    """
    def __init__(
        self,
        content_encryption_key: bytes,
        data_stream: BinaryIO,
    ):
        self.content_encryption_key = content_encryption_key
        self.data_stream = data_stream

        self.offset = 0
        self.current = b''
        self.nonce_counter = 0

    def read(self, size: int = -1) -> bytes:
        """
        Read data from the stream. Specify -1 to read all available data.

        :param int size: The amount of data to read. Defaults to -1 for all data.
        :return: The bytes read.
        :rtype: bytes
        """
        result = BytesIO()
        remaining = sys.maxsize if size == -1 else size

        while remaining > 0:
            # Start by reading from current
            if len(self.current) > 0:
                read = min(remaining, len(self.current))
                result.write(self.current[:read])

                self.current = self.current[read:]
                self.offset += read
                remaining -= read

            if remaining > 0:
                # Read one region of data and encrypt it
                data = self.data_stream.read(_GCM_REGION_DATA_LENGTH)
                if len(data) == 0:
                    # No more data to read
                    break

                self.current = self._encrypt_region(data)

        return result.getvalue()

    def _encrypt_region(self, data: bytes) -> bytes:
        """
        Encrypt the given region of data using AES-GCM. The result
        includes the data in the form: nonce + ciphertext + tag.

        :param bytes data: The data to encrypt.
        :return: The encrypted bytes.
        :rtype: bytes
        """
        # Each region MUST use a different nonce
        nonce = self.nonce_counter.to_bytes(_GCM_NONCE_LENGTH, 'big')
        self.nonce_counter += 1

        aesgcm = AESGCM(self.content_encryption_key)

        # Returns ciphertext + tag
        ciphertext_with_tag = aesgcm.encrypt(nonce, data, None)
        return nonce + ciphertext_with_tag


def is_encryption_v2(encryption_data: Optional[_EncryptionData]) -> bool:
    """
    Determine whether the given encryption data signifies version 2.0.

    :param Optional[_EncryptionData] encryption_data: The encryption data. Will return False if this is None.
    :return: True, if the encryption data indicates encryption V2, false otherwise.
    :rtype: bool
    """
    # If encryption_data is None, assume no encryption
    return encryption_data and encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V2


def modify_user_agent_for_encryption(
        user_agent: str,
        moniker: str,
        encryption_version: str,
        request_options: Dict[str, Any]
    ) -> None:
    """
    Modifies the request options to contain a user agent string updated with encryption information.
    Adds azstorage-clientsideencryption/<version> immediately proceeding the SDK descriptor.

    :param str user_agent: The existing User Agent to modify.
    :param str moniker: The specific SDK moniker. The modification will immediately proceed azsdk-python-{moniker}.
    :param str encryption_version: The version of encryption being used.
    :param Dict[str, Any] request_options: The reuqest options to add the user agent override to.
    """
    # If the user has specified user_agent_overwrite=True, don't make any modifications
    if request_options.get('user_agent_overwrite'):
        return

    # If the feature flag is already present, don't add it again
    feature_flag = f"azstorage-clientsideencryption/{encryption_version}"
    if feature_flag in user_agent:
        return

    index = user_agent.find(f"azsdk-python-{moniker}")
    user_agent = f"{user_agent[:index]}{feature_flag} {user_agent[index:]}"
    # Since we are using user_agent_overwrite=True, we must prepend the user's user_agent if there is one
    if request_options.get('user_agent'):
        user_agent = f"{request_options.get('user_agent')} {user_agent}"

    request_options['user_agent'] = user_agent
    request_options['user_agent_overwrite'] = True


def get_adjusted_upload_size(length: int, encryption_version: str) -> int:
    """
    Get the adjusted size of the blob upload which accounts for
    extra encryption data (padding OR nonce + tag).

    :param int length: The plaintext data length.
    :param str encryption_version: The version of encryption being used.
    :return: The new upload size to use.
    :rtype: int
    """
    if encryption_version == _ENCRYPTION_PROTOCOL_V1:
        return length + (16 - (length % 16))

    if encryption_version == _ENCRYPTION_PROTOCOL_V2:
        encryption_data_length = _GCM_NONCE_LENGTH + _GCM_TAG_LENGTH
        regions = math.ceil(length / _GCM_REGION_DATA_LENGTH)
        return length + (regions * encryption_data_length)

    raise ValueError("Invalid encryption version specified.")


def get_adjusted_download_range_and_offset(
        start: int,
        end: int,
        length: int,
        encryption_data: Optional[_EncryptionData]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Gets the new download range and offsets into the decrypted data for
    the given user-specified range. The new download range will include all
    the data needed to decrypt the user-provided range and will include only
    full encryption regions.

    The offsets returned will be the offsets needed to fetch the user-requested
    data out of the full decrypted data. The end offset is different based on the
    encryption version. For V1, the end offset is offset from the end whereas for
    V2, the end offset is the ending index into the stream.
    V1: decrypted_data[start_offset : len(decrypted_data) - end_offset]
    V2: decrypted_data[start_offset : end_offset]

    :param int start: The user-requested start index.
    :param int end: The user-requested end index.
    :param int length: The user-requested length. Only used for V1.
    :param Optional[_EncryptionData] encryption_data: The encryption data to determine version and sizes.
    :return: (new start, new end), (start offset, end offset)
    :rtype: Tuple[Tuple[int, int], Tuple[int, int]]
    """
    start_offset, end_offset = 0, 0
    if encryption_data is None:
        return (start, end), (start_offset, end_offset)

    if encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V1:
        if start is not None:
            # Align the start of the range along a 16 byte block
            start_offset = start % 16
            start -= start_offset

            # Include an extra 16 bytes for the IV if necessary
            # Because of the previous offsetting, start_range will always
            # be a multiple of 16.
            if start > 0:
                start_offset += 16
                start -= 16

        if length is not None:
            # Align the end of the range along a 16 byte block
            end_offset = 15 - (end % 16)
            end += end_offset

    elif encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V2:
        start_offset, end_offset = 0, end

        nonce_length = encryption_data.encrypted_region_info.nonce_length
        data_length = encryption_data.encrypted_region_info.data_length
        tag_length = encryption_data.encrypted_region_info.tag_length
        region_length = nonce_length + data_length + tag_length
        requested_length = end - start

        if start is not None:
            # Find which data region the start is in
            region_num = start // data_length
            # The start of the data region is different from the start of the encryption region
            data_start = region_num * data_length
            region_start = region_num * region_length
            # Offset is based on data region
            start_offset = start - data_start
            # New start is the start of the encryption region
            start = region_start

        if end is not None:
            # Find which data region the end is in
            region_num = end // data_length
            end_offset = start_offset + requested_length + 1
            # New end is the end of the encryption region
            end = (region_num * region_length) + region_length - 1

    return (start, end), (start_offset, end_offset)


def parse_encryption_data(metadata: Dict[str, Any]) -> Optional[_EncryptionData]:
    """
    Parses the encryption data out of the given blob metadata. If metadata does
    not exist or there are parsing errors, this function will just return None.

    :param Dict[str, Any] metadata: The blob metadata parsed from the response.
    :return: The encryption data or None
    :rtype: Optional[_EncryptionData]
    """
    try:
        # Use case insensitive dict as key needs to be case-insensitive
        case_insensitive_metadata = CaseInsensitiveDict(metadata)
        return _dict_to_encryption_data(loads(case_insensitive_metadata['encryptiondata']))
    except:  # pylint: disable=bare-except
        return None


def adjust_blob_size_for_encryption(size: int, encryption_data: Optional[_EncryptionData]) -> int:
    """
    Adjusts the given blob size for encryption by subtracting the size of
    the encryption data (nonce + tag). This only has an affect for encryption V2.

    :param int size: The original blob size.
    :param Optional[_EncryptionData] encryption_data: The encryption data to determine version and sizes.
    :return: The new blob size.
    :rtype: int
    """
    if is_encryption_v2(encryption_data):
        nonce_length = encryption_data.encrypted_region_info.nonce_length
        data_length = encryption_data.encrypted_region_info.data_length
        tag_length = encryption_data.encrypted_region_info.tag_length
        region_length = nonce_length + data_length + tag_length

        num_regions = math.ceil(size / region_length)
        metadata_size = num_regions * (nonce_length + tag_length)
        return size - metadata_size

    return size


def _generate_encryption_data_dict(kek, cek, iv, version):
    '''
    Generates and returns the encryption metadata as a dict.

    :param object kek: The key encryption key. See calling functions for more information.
    :param bytes cek: The content encryption key.
    :param Optional[bytes] iv: The initialization vector. Only required for AES-CBC.
    :param str version: The client encryption version used.
    :return: A dict containing all the encryption metadata.
    :rtype: dict
    '''
    # Encrypt the cek.
    if version == _ENCRYPTION_PROTOCOL_V1:
        wrapped_cek = kek.wrap_key(cek)
    # For V2, we include the encryption version in the wrapped key.
    elif version == _ENCRYPTION_PROTOCOL_V2:
        # We must pad the version to 8 bytes for AES Keywrap algorithms
        to_wrap = _ENCRYPTION_PROTOCOL_V2.encode().ljust(8, b'\0') + cek
        wrapped_cek = kek.wrap_key(to_wrap)

    # Build the encryption_data dict.
    # Use OrderedDict to comply with Java's ordering requirement.
    wrapped_content_key = OrderedDict()
    wrapped_content_key['KeyId'] = kek.get_kid()
    wrapped_content_key['EncryptedKey'] = encode_base64(wrapped_cek)
    wrapped_content_key['Algorithm'] = kek.get_key_wrap_algorithm()

    encryption_agent = OrderedDict()
    encryption_agent['Protocol'] = version

    if version == _ENCRYPTION_PROTOCOL_V1:
        encryption_agent['EncryptionAlgorithm'] = _EncryptionAlgorithm.AES_CBC_256

    elif version == _ENCRYPTION_PROTOCOL_V2:
        encryption_agent['EncryptionAlgorithm'] = _EncryptionAlgorithm.AES_GCM_256

        encrypted_region_info = OrderedDict()
        encrypted_region_info['DataLength'] = _GCM_REGION_DATA_LENGTH
        encrypted_region_info['NonceLength'] = _GCM_NONCE_LENGTH

    encryption_data_dict = OrderedDict()
    encryption_data_dict['WrappedContentKey'] = wrapped_content_key
    encryption_data_dict['EncryptionAgent'] = encryption_agent
    if version == _ENCRYPTION_PROTOCOL_V1:
        encryption_data_dict['ContentEncryptionIV'] = encode_base64(iv)
    elif version == _ENCRYPTION_PROTOCOL_V2:
        encryption_data_dict['EncryptedRegionInfo'] = encrypted_region_info
    encryption_data_dict['KeyWrappingMetadata'] = {'EncryptionLibrary': 'Python ' + VERSION}

    return encryption_data_dict


def _dict_to_encryption_data(encryption_data_dict):
    '''
    Converts the specified dictionary to an EncryptionData object for
    eventual use in decryption.

    :param dict encryption_data_dict:
        The dictionary containing the encryption data.
    :return: an _EncryptionData object built from the dictionary.
    :rtype: _EncryptionData
    '''
    try:
        protocol = encryption_data_dict['EncryptionAgent']['Protocol']
        if protocol not in [_ENCRYPTION_PROTOCOL_V1, _ENCRYPTION_PROTOCOL_V2]:
            raise ValueError("Unsupported encryption version.")
    except KeyError as exc:
        raise ValueError("Unsupported encryption version.") from exc
    wrapped_content_key = encryption_data_dict['WrappedContentKey']
    wrapped_content_key = _WrappedContentKey(wrapped_content_key['Algorithm'],
                                             decode_base64_to_bytes(wrapped_content_key['EncryptedKey']),
                                             wrapped_content_key['KeyId'])

    encryption_agent = encryption_data_dict['EncryptionAgent']
    encryption_agent = _EncryptionAgent(encryption_agent['EncryptionAlgorithm'],
                                        encryption_agent['Protocol'])

    if 'KeyWrappingMetadata' in encryption_data_dict:
        key_wrapping_metadata = encryption_data_dict['KeyWrappingMetadata']
    else:
        key_wrapping_metadata = None

    # AES-CBC only
    encryption_iv = None
    if 'ContentEncryptionIV' in encryption_data_dict:
        encryption_iv = decode_base64_to_bytes(encryption_data_dict['ContentEncryptionIV'])

    # AES-GCM only
    region_info = None
    if 'EncryptedRegionInfo' in encryption_data_dict:
        encrypted_region_info = encryption_data_dict['EncryptedRegionInfo']
        region_info = _EncryptedRegionInfo(encrypted_region_info['DataLength'],
                                           encrypted_region_info['NonceLength'],
                                           _GCM_TAG_LENGTH)

    encryption_data = _EncryptionData(encryption_iv,
                                      region_info,
                                      encryption_agent,
                                      wrapped_content_key,
                                      key_wrapping_metadata)

    return encryption_data


def _generate_AES_CBC_cipher(cek, iv):
    '''
    Generates and returns an encryption cipher for AES CBC using the given cek and iv.

    :param bytes[] cek: The content encryption key for the cipher.
    :param bytes[] iv: The initialization vector for the cipher.
    :return: A cipher for encrypting in AES256 CBC.
    :rtype: ~cryptography.hazmat.primitives.ciphers.Cipher
    '''

    backend = default_backend()
    algorithm = AES(cek)
    mode = CBC(iv)
    return Cipher(algorithm, mode, backend)


def _validate_and_unwrap_cek(encryption_data, key_encryption_key=None, key_resolver=None):
    '''
    Extracts and returns the content_encryption_key stored in the encryption_data object
    and performs necessary validation on all parameters.
    :param _EncryptionData encryption_data:
        The encryption metadata of the retrieved value.
    :param obj key_encryption_key:
        The key_encryption_key used to unwrap the cek. Please refer to high-level service object
        instance variables for more details.
    :param func key_resolver:
        A function used that, given a key_id, will return a key_encryption_key. Please refer
        to high-level service object instance variables for more details.
    :return: the content_encryption_key stored in the encryption_data object.
    :rtype: bytes[]
    '''

    _validate_not_none('encrypted_key', encryption_data.wrapped_content_key.encrypted_key)

    # Validate we have the right info for the specified version
    if encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V1:
        _validate_not_none('content_encryption_IV', encryption_data.content_encryption_IV)
    elif encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V2:
        _validate_not_none('encrypted_region_info', encryption_data.encrypted_region_info)
    else:
        raise ValueError('Specified encryption version is not supported.')

    content_encryption_key = None

    # If the resolver exists, give priority to the key it finds.
    if key_resolver is not None:
        key_encryption_key = key_resolver(encryption_data.wrapped_content_key.key_id)

    _validate_not_none('key_encryption_key', key_encryption_key)
    if not hasattr(key_encryption_key, 'get_kid') or not callable(key_encryption_key.get_kid):
        raise AttributeError(_ERROR_OBJECT_INVALID.format('key encryption key', 'get_kid'))
    if not hasattr(key_encryption_key, 'unwrap_key') or not callable(key_encryption_key.unwrap_key):
        raise AttributeError(_ERROR_OBJECT_INVALID.format('key encryption key', 'unwrap_key'))
    if encryption_data.wrapped_content_key.key_id != key_encryption_key.get_kid():
        raise ValueError('Provided or resolved key-encryption-key does not match the id of key used to encrypt.')
    # Will throw an exception if the specified algorithm is not supported.
    content_encryption_key = key_encryption_key.unwrap_key(encryption_data.wrapped_content_key.encrypted_key,
                                                           encryption_data.wrapped_content_key.algorithm)

    # For V2, the version is included with the cek. We need to validate it
    # and remove it from the actual cek.
    if encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V2:
        version_2_bytes = _ENCRYPTION_PROTOCOL_V2.encode().ljust(8, b'\0')
        cek_version_bytes = content_encryption_key[:len(version_2_bytes)]
        if cek_version_bytes != version_2_bytes:
            raise ValueError('The encryption metadata is not valid and may have been modified.')

        # Remove version from the start of the cek.
        content_encryption_key = content_encryption_key[len(version_2_bytes):]

    _validate_not_none('content_encryption_key', content_encryption_key)

    return content_encryption_key


def _decrypt_message(message, encryption_data, key_encryption_key=None, resolver=None):
    """
    Decrypts the given ciphertext using AES256 in CBC mode with 128 bit padding.
    Unwraps the content-encryption-key using the user-provided or resolved key-encryption-key (kek).
    Returns the original plaintex.

    :param str message:
        The ciphertext to be decrypted.
    :param _EncryptionData encryption_data:
        The metadata associated with this ciphertext.
    :param object key_encryption_key:
        The user-provided key-encryption-key. Must implement the following methods:
        unwrap_key(key, algorithm)
            - returns the unwrapped form of the specified symmetric key using the string-specified algorithm.
        get_kid()
            - returns a string key id for this key-encryption-key.
    :param Callable resolver:
        The user-provided key resolver. Uses the kid string to return a key-encryption-key
        implementing the interface defined above.
    :return: The decrypted plaintext.
    :rtype: str
    """
    _validate_not_none('message', message)
    content_encryption_key = _validate_and_unwrap_cek(encryption_data, key_encryption_key, resolver)

    if encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V1:
        if not encryption_data.content_encryption_IV:
            raise ValueError("Missing required metadata for decryption.")

        cipher = _generate_AES_CBC_cipher(content_encryption_key, encryption_data.content_encryption_IV)

        # decrypt data
        decrypted_data = message
        decryptor = cipher.decryptor()
        decrypted_data = (decryptor.update(decrypted_data) + decryptor.finalize())

        # unpad data
        unpadder = PKCS7(128).unpadder()
        decrypted_data = (unpadder.update(decrypted_data) + unpadder.finalize())

    elif encryption_data.encryption_agent.protocol == _ENCRYPTION_PROTOCOL_V2:
        block_info = encryption_data.encrypted_region_info
        if not block_info or not block_info.nonce_length:
            raise ValueError("Missing required metadata for decryption.")

        nonce_length = encryption_data.encrypted_region_info.nonce_length

        # First bytes are the nonce
        nonce = message[:nonce_length]
        ciphertext_with_tag = message[nonce_length:]

        aesgcm = AESGCM(content_encryption_key)
        decrypted_data = aesgcm.decrypt(nonce, ciphertext_with_tag, None)

    else:
        raise ValueError('Specified encryption version is not supported.')

    return decrypted_data


def encrypt_blob(blob, key_encryption_key, version):
    '''
    Encrypts the given blob using the given encryption protocol version.
    Wraps the generated content-encryption-key using the user-provided key-encryption-key (kek).
    Returns a json-formatted string containing the encryption metadata. This method should
    only be used when a blob is small enough for single shot upload. Encrypting larger blobs
    is done as a part of the upload_data_chunks method.

    :param bytes blob:
        The blob to be encrypted.
    :param object key_encryption_key:
        The user-provided key-encryption-key. Must implement the following methods:
        wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
        get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
        get_kid()--returns a string key id for this key-encryption-key.
    :param str version: The client encryption version to use.
    :return: A tuple of json-formatted string containing the encryption metadata and the encrypted blob data.
    :rtype: (str, bytes)
    '''

    _validate_not_none('blob', blob)
    _validate_not_none('key_encryption_key', key_encryption_key)
    _validate_key_encryption_key_wrap(key_encryption_key)

    if version == _ENCRYPTION_PROTOCOL_V1:
        # AES256 uses 256 bit (32 byte) keys and always with 16 byte blocks
        content_encryption_key = os.urandom(32)
        initialization_vector = os.urandom(16)

        cipher = _generate_AES_CBC_cipher(content_encryption_key, initialization_vector)

        # PKCS7 with 16 byte blocks ensures compatibility with AES.
        padder = PKCS7(128).padder()
        padded_data = padder.update(blob) + padder.finalize()

        # Encrypt the data.
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    elif version == _ENCRYPTION_PROTOCOL_V2:
        # AES256 GCM uses 256 bit (32 byte) keys and a 12 byte nonce.
        content_encryption_key = os.urandom(32)
        initialization_vector = None

        data = BytesIO(blob)
        encryption_stream = GCMBlobEncryptionStream(content_encryption_key, data)

        encrypted_data = encryption_stream.read()

    else:
        raise ValueError("Invalid encryption version specified.")

    encryption_data = _generate_encryption_data_dict(key_encryption_key, content_encryption_key,
                                                     initialization_vector, version)
    encryption_data['EncryptionMode'] = 'FullBlob'

    return dumps(encryption_data), encrypted_data


def generate_blob_encryption_data(key_encryption_key, version):
    '''
    Generates the encryption_metadata for the blob.

    :param object key_encryption_key:
        The key-encryption-key used to wrap the cek associate with this blob.
    :param str version: The client encryption version to use.
    :return: A tuple containing the cek and iv for this blob as well as the
        serialized encryption metadata for the blob.
    :rtype: (bytes, Optional[bytes], str)
    '''
    encryption_data = None
    content_encryption_key = None
    initialization_vector = None
    if key_encryption_key:
        _validate_key_encryption_key_wrap(key_encryption_key)
        content_encryption_key = os.urandom(32)
        # Initialization vector only needed for V1
        if version == _ENCRYPTION_PROTOCOL_V1:
            initialization_vector = os.urandom(16)
        encryption_data = _generate_encryption_data_dict(key_encryption_key,
                                                         content_encryption_key,
                                                         initialization_vector,
                                                         version)
        encryption_data['EncryptionMode'] = 'FullBlob'
        encryption_data = dumps(encryption_data)

    return content_encryption_key, initialization_vector, encryption_data


def decrypt_blob(  # pylint: disable=too-many-locals,too-many-statements
        require_encryption,
        key_encryption_key,
        key_resolver,
        content,
        start_offset,
        end_offset,
        response_headers):
    """
    Decrypts the given blob contents and returns only the requested range.

    :param bool require_encryption:
        Whether the calling blob service requires objects to be decrypted.
    :param object key_encryption_key:
        The user-provided key-encryption-key. Must implement the following methods:
        wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
        get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
        get_kid()--returns a string key id for this key-encryption-key.
    :param object key_resolver:
        The user-provided key resolver. Uses the kid string to return a key-encryption-key
        implementing the interface defined above.
    :param bytes content:
        The encrypted blob content.
    :param int start_offset:
        The adjusted offset from the beginning of the *decrypted* content for the caller's data.
    :param int end_offset:
        The adjusted offset from the end of the *decrypted* content for the caller's data.
    :param Dict[str, Any] response_headers:
        A dictionary of response headers from the download request. Expected to include the
        'x-ms-meta-encryptiondata' header if the blob was encrypted.
    :return: The decrypted blob content.
    :rtype: bytes
    """
    try:
        encryption_data = _dict_to_encryption_data(loads(response_headers['x-ms-meta-encryptiondata']))
    except Exception as exc:  # pylint: disable=broad-except
        if require_encryption:
            raise ValueError(
                'Encryption required, but received data does not contain appropriate metadata.' + \
                'Data was either not encrypted or metadata has been lost.') from exc

        return content

    algorithm = encryption_data.encryption_agent.encryption_algorithm
    if algorithm not in(_EncryptionAlgorithm.AES_CBC_256, _EncryptionAlgorithm.AES_GCM_256):
        raise ValueError('Specified encryption algorithm is not supported.')

    version = encryption_data.encryption_agent.protocol
    if version not in (_ENCRYPTION_PROTOCOL_V1, _ENCRYPTION_PROTOCOL_V2):
        raise ValueError('Specified encryption version is not supported.')

    content_encryption_key = _validate_and_unwrap_cek(encryption_data, key_encryption_key, key_resolver)

    if version == _ENCRYPTION_PROTOCOL_V1:
        blob_type = response_headers['x-ms-blob-type']

        iv = None
        unpad = False
        if 'content-range' in response_headers:
            content_range = response_headers['content-range']
            # Format: 'bytes x-y/size'

            # Ignore the word 'bytes'
            content_range = content_range.split(' ')

            content_range = content_range[1].split('-')
            content_range = content_range[1].split('/')
            end_range = int(content_range[0])
            blob_size = int(content_range[1])

            if start_offset >= 16:
                iv = content[:16]
                content = content[16:]
                start_offset -= 16
            else:
                iv = encryption_data.content_encryption_IV

            if end_range == blob_size - 1:
                unpad = True
        else:
            unpad = True
            iv = encryption_data.content_encryption_IV

        if blob_type == 'PageBlob':
            unpad = False

        cipher = _generate_AES_CBC_cipher(content_encryption_key, iv)
        decryptor = cipher.decryptor()

        content = decryptor.update(content) + decryptor.finalize()
        if unpad:
            unpadder = PKCS7(128).unpadder()
            content = unpadder.update(content) + unpadder.finalize()

        return content[start_offset: len(content) - end_offset]

    if version == _ENCRYPTION_PROTOCOL_V2:
        # We assume the content contains only full encryption regions
        total_size = len(content)
        offset = 0

        nonce_length = encryption_data.encrypted_region_info.nonce_length
        data_length = encryption_data.encrypted_region_info.data_length
        tag_length = encryption_data.encrypted_region_info.tag_length
        region_length = nonce_length + data_length + tag_length

        decrypted_content = bytearray()
        while offset < total_size:
            # Process one encryption region at a time
            process_size = min(region_length, total_size)
            encrypted_region = content[offset:offset + process_size]

            # First bytes are the nonce
            nonce = encrypted_region[:nonce_length]
            ciphertext_with_tag = encrypted_region[nonce_length:]

            aesgcm = AESGCM(content_encryption_key)
            decrypted_data = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
            decrypted_content.extend(decrypted_data)

            offset += process_size

        # Read the caller requested data from the decrypted content
        return decrypted_content[start_offset:end_offset]

    raise ValueError('Specified encryption version is not supported.')


def get_blob_encryptor_and_padder(cek, iv, should_pad):
    encryptor = None
    padder = None

    if cek is not None and iv is not None:
        cipher = _generate_AES_CBC_cipher(cek, iv)
        encryptor = cipher.encryptor()
        padder = PKCS7(128).padder() if should_pad else None

    return encryptor, padder


def encrypt_queue_message(message, key_encryption_key, version):
    '''
    Encrypts the given plain text message using the given protocol version.
    Wraps the generated content-encryption-key using the user-provided key-encryption-key (kek).
    Returns a json-formatted string containing the encrypted message and the encryption metadata.

    :param object message:
        The plain text message to be encrypted.
    :param object key_encryption_key:
        The user-provided key-encryption-key. Must implement the following methods:
        wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
        get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
        get_kid()--returns a string key id for this key-encryption-key.
    :param str version: The client encryption version to use.
    :return: A json-formatted string containing the encrypted message and the encryption metadata.
    :rtype: str
    '''

    _validate_not_none('message', message)
    _validate_not_none('key_encryption_key', key_encryption_key)
    _validate_key_encryption_key_wrap(key_encryption_key)

    # Queue encoding functions all return unicode strings, and encryption should
    # operate on binary strings.
    message = message.encode('utf-8')

    if version == _ENCRYPTION_PROTOCOL_V1:
        # AES256 CBC uses 256 bit (32 byte) keys and always with 16 byte blocks
        content_encryption_key = os.urandom(32)
        initialization_vector = os.urandom(16)

        cipher = _generate_AES_CBC_cipher(content_encryption_key, initialization_vector)

        # PKCS7 with 16 byte blocks ensures compatibility with AES.
        padder = PKCS7(128).padder()
        padded_data = padder.update(message) + padder.finalize()

        # Encrypt the data.
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    elif version == _ENCRYPTION_PROTOCOL_V2:
        # AES256 GCM uses 256 bit (32 byte) keys and a 12 byte nonce.
        content_encryption_key = os.urandom(32)
        initialization_vector = None

        # The nonce MUST be different for each key
        nonce = os.urandom(12)
        aesgcm = AESGCM(content_encryption_key)

        # Returns ciphertext + tag
        ciphertext_with_tag = aesgcm.encrypt(nonce, message, None)
        encrypted_data = nonce + ciphertext_with_tag

    else:
        raise ValueError("Invalid encryption version specified.")

    # Build the dictionary structure.
    queue_message = {'EncryptedMessageContents': encode_base64(encrypted_data),
                     'EncryptionData': _generate_encryption_data_dict(key_encryption_key,
                                                                      content_encryption_key,
                                                                      initialization_vector,
                                                                      version)}

    return dumps(queue_message)


def decrypt_queue_message(message, response, require_encryption, key_encryption_key, resolver):
    """
    Returns the decrypted message contents from an EncryptedQueueMessage.
    If no encryption metadata is present, will return the unaltered message.
    :param str message:
        The JSON formatted QueueEncryptedMessage contents with all associated metadata.
    :param Any response:
        The pipeline response used to generate an error with.
    :param bool require_encryption:
        If set, will enforce that the retrieved messages are encrypted and decrypt them.
    :param object key_encryption_key:
        The user-provided key-encryption-key. Must implement the following methods:
        unwrap_key(key, algorithm)
            - returns the unwrapped form of the specified symmetric key usingthe string-specified algorithm.
        get_kid()
            - returns a string key id for this key-encryption-key.
    :param Callable resolver:
        The user-provided key resolver. Uses the kid string to return a key-encryption-key
        implementing the interface defined above.
    :return: The plain text message from the queue message.
    :rtype: str
    """
    response = response.http_response

    try:
        message = loads(message)

        encryption_data = _dict_to_encryption_data(message['EncryptionData'])
        decoded_data = decode_base64_to_bytes(message['EncryptedMessageContents'])
    except (KeyError, ValueError) as exc:
        # Message was not json formatted and so was not encrypted
        # or the user provided a json formatted message
        # or the metadata was malformed.
        if require_encryption:
            raise ValueError(
                'Encryption required, but received message does not contain appropriate metatadata. ' + \
                'Message was either not encrypted or metadata was incorrect.') from exc

        return message
    try:
        return _decrypt_message(decoded_data, encryption_data, key_encryption_key, resolver).decode('utf-8')
    except Exception as error:
        raise HttpResponseError(
            message="Decryption failed.",
            response=response,
            error=error) from error
