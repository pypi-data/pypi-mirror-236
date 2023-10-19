# Installation
```shell
pip install -U xrypt-xethhung12
```

# Usage
```shell
from xrypt_xethhung12.xrypt import load_pub, load_pri, hybrid_encrypt, hybrid_decrypt

sender_pub = load_pub("rsa_public_key.pem")
sender_pri = load_pri("rsa_private_key.pem")

receiver_pub = load_pub("rsa_public_key_2.pem")
receiver_pri = load_pri("rsa_private_key_2.pem")

# normal case
key_str,iv_str,encrypt_data,sign = hybrid_encrypt(receiver_pub, sender_pri, "abcd1234567890".encode("utf-8"))
decrypted_data = hybrid_decrypt(receiver_pri, sender_pub, key_str, iv_str, encrypt_data, sign)
# decrypted_data -> b'abcd1234567890'

# incase the verify key fail
# there will be a exception raised
```

# Scripts

## Generate rsa key pair
```shell
pri={pri}
pub={pub}
openssl genrsa -out $pri 4096
openssl rsa -in $pri -outform PEM -pubout -out $pub
```

## Build 
```shell
rm -fr dist
python3 -m build
```


## Build and Deploy
```shell
rm -fr dist
python3 -m build
twine upload dist/* -u __token__ -p $pwd
```

## Update version dev
```shell
python3 -m xh_py_project_versioning --patch
```

## Update version
```shell
python3 -m xh_py_project_versioning --patch -d
```
