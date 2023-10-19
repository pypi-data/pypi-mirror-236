from pg_common import rand_str
import base64
from Crypto.Cipher import AES

__INIT_NUM__ = 100000000
__XOR_NUM__ = 0xF0F0F0

__all__ = ["uid_encode", "uid_decode", "aes_encrypt", "aes_decrypt"]
__auth__ = "baozilaji@gmail.com"

__BLOCK_SIZE__ = 16
__padding__ = lambda s: s + (__BLOCK_SIZE__ - len(s) % __BLOCK_SIZE__) * chr(__BLOCK_SIZE__ - len(s) % __BLOCK_SIZE__)
__unpadding__ = lambda s: s[0:-(s[-1])]


def uid_encode(uid):
    if not uid:
        return 0
    return (uid ^ __XOR_NUM__) + __INIT_NUM__


def uid_decode(pid):
    if not pid:
        return 0
    return (pid - __INIT_NUM__) ^ __XOR_NUM__


# aes encrypt data using ecb mode
def aes_encrypt(src_data):
    _key = rand_str(_len=16)
    _cipher = AES.new(_key, AES.MODE_ECB)
    _encrypted_data = _cipher.encrypt(__padding__(src_data))
    return _key+base64.b64encode(_encrypted_data).decode()


# aes decrypt data using ecb mode
def aes_decrypt(dst_data):
    _key = dst_data[0:16]
    _base64_data = dst_data[16:]
    _aes_encrypted_data = base64.b64decode(_base64_data)
    _cipher = AES.new(_key, AES.MODE_ECB)
    return __unpadding__(_cipher.decrypt(_aes_encrypted_data)).decode()
