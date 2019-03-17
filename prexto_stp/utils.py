import base64
import locale
import os
import OpenSSL.crypto as ct 
import re

from .settings import STP, BASE_DIR


utf8_encode = lambda t: str(t).encode()

def clean_and_cut_text(text, length):
    text = str(text)
    return clean_text(text[:length])

def clean_text(text):
    unwanted_array = {"Å ":"S", "Å¡":"s", "Å½":"Z", "Å¾":"z", "Ã€":"A", "Ã":"A", "Ã‚":"A", "Ãƒ":"A", "Ã„":"A", "Ã…":"A", "Ã†":"A", "Ã‡":"C", "Ãˆ":"E", "Ã‰":"E",
    "ÃŠ":"E", "Ã‹":"E", "ÃŒ":"I", "Ã":"I", "ÃŽ":"I", "Ã":"I", "Ã‘":"N", "Ã’":"O", "Ã“":"O", "Ã”":"O", "Ã•":"O", "Ã–":"O", "Ã˜":"O", "Ã™":"U",
    "Ãš":"U", "Ã›":"U", "Ãœ":"U", "Ã":"Y", "Ãž":"B", "ÃŸ":"Ss", "Ã ":"a", "Ã¡":"a", "Ã¢":"a", "Ã£":"a", "Ã¤":"a", "Ã¥":"a", "Ã¦":"a", "Ã§":"c",
    "Ã¨":"e", "Ã©":"e", "Ãª":"e", "Ã«":"e", "Ã¬":"i", "Ã­":"i", "Ã®":"i", "Ã¯":"i", "Ã°":"o", "Ã±":"n", "Ã²":"o", "Ã³":"o", "Ã´":"o", "Ãµ":"o",
    "Ã¶":"o", "Ã¸":"o", "Ã¹":"u", "Ãº":"u", "Ã»":"u", "Ã½":"y", "Ã¾":"b", "Ã¿":"y", "á": "a", "Á": "A", "ó": "o", "Ó": "O", "é": "e", "É": "E", "í": "i", "Í": "I", "ú": "u", "Ú": "U"}
    return strtr(text, unwanted_array)

def number_format(num, places=0):
    return locale.format("%.*f", (places, num), True)

def strtr(s, repl):
    pattern = '|'.join(map(re.escape, sorted(repl, key=len, reverse=True)))
    return re.sub(pattern, lambda m: repl[m.group()], s)

class Signer(object):
    @staticmethod
    def sign(data_to_sign):
        p_key_id = Signer.get_certified()
        data_signed = ct.sign(p_key_id, data_to_sign, STP['signature']) 
        return base64.b64encode(data_signed).decode('utf-8')

    @staticmethod
    def get_certified():
        pemfile = os.path.join(BASE_DIR, STP['pemfile'])

        if not os.path.exists(pemfile):
            raise Exception('The file {} doesn\'t exist!'.format(pemfile))

        with open(pemfile) as file:
            return ct.load_privatekey(type=ct.FILETYPE_PEM, buffer=file.read(), passphrase=str.encode(STP['passphrase']))
