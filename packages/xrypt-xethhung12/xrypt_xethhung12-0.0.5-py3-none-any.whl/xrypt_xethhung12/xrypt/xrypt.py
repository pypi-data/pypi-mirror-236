from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
import base64

def load_pub(file):
    with open(file, "r") as f:
        return RSA.import_key(f.read())


def load_pri(file):
    with open(file, "r") as f:
        return RSA.import_key(f.read())


def hybrid_encrypt(sender_key, receiver_key, data,
                   get_cipher=lambda key: PKCS1_OAEP.new(key),
                   get_signer=lambda key: PKCS1_v1_5.new(key)
                   ):
    sender_cipher = get_cipher(sender_key)
    receiver_signer = get_signer(receiver_key)
    to_b64_str = lambda x: base64.b64encode(x).decode("utf-8")
    key = Random.new().read(32)
    key_str = to_b64_str(sender_cipher.encrypt(key))
    iv = Random.new().read(AES.block_size)
    iv_str = to_b64_str(sender_cipher.encrypt(iv))
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypt_data = to_b64_str(aes.encrypt(pad(data, AES.block_size)))

    digest = SHA512.new()
    digest.update(data)
    sign = base64.b64encode(receiver_signer.sign(digest)).decode("utf-8")

    return (key_str, iv_str, encrypt_data, sign)


def hybrid_decrypt(receiver_key, sender_key, key_str, iv_str, data_str, sign, check_sign=True,
                   get_cipher=lambda key: PKCS1_OAEP.new(key),
                   get_verifier=lambda key: PKCS1_v1_5.new(key)
                   ):
    receiver_cipher = get_cipher(receiver_key)
    sender_verifier = get_verifier(sender_key)
    key = receiver_cipher.decrypt(base64.b64decode(key_str.encode("utf-8")))
    iv = receiver_cipher.decrypt(base64.b64decode(iv_str.encode("utf-8")))

    aes = AES.new(key, AES.MODE_CBC, iv)

    data = unpad(aes.decrypt(base64.b64decode(data_str.encode("utf-8"))), AES.block_size)

    if check_sign:
        digest = SHA512.new()
        digest.update(data)
        valid = sender_verifier.verify(digest, base64.b64decode(sign.encode("utf-8")))
        if not valid:
            raise Exception("Fail to pass signature")

    return data
