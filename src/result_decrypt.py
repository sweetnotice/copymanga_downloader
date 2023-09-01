import re
import json
import base64
import binascii
from Crypto.Cipher import AES


def deaes_cbc(data: str, key: str, iv: str):
    def add_16(par):  # 补位到16倍数位
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    # 对key进行补位 。key，iv 进行编码，把data编码成字节
    key = add_16(key.encode('utf-8'))
    iv = iv.encode('utf-8')
    if '/' in data or '+' in data or '=' in data:  # 为普通字节
        data = base64.decodebytes(data.encode('utf-8'))
    else:
        data = binascii.a2b_hex(data.encode('utf-8'))  # 为十六位数
    aes = AES.new(key, AES.MODE_CBC, iv)
    text = aes.decrypt(data)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', "", text.decode('utf-8'))
    return text


def mange_decrypt(encrypt_data: str) -> dict:
    decrypt_data = json.loads(deaes_cbc(encrypt_data[16:], 'xxxmanga.woo.key', encrypt_data[:16]))
    return decrypt_data