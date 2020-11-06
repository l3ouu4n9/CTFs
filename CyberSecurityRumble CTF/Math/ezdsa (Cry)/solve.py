# https://crypto.stackexchange.com/questions/57846/recovering-private-key-from-secp256k1-signatures
import ecdsa, hashlib
from ecdsa.numbertheory import inverse_mod
from ecdsa.ecdsa import Signature
from ecdsa import SigningKey, VerifyingKey, der
from pwn import *

curve          = ecdsa.SECP256k1
text_to_sign   = b"admin"
hash_algorithm = hashlib.sha1

def get_key_from_hash():

    # sha1(god)
    m_hash1 = '21298df8a3277357ee55b01df9530b535cf08ec1'
    # nc chal.cybersecurityrumble.de 10101
    # god
    # Your token: god,9f2f2061e1898665c6ae49e665bc5f344a6005104c242d53f74c8548de7a468502ac0b1b2e9be9f26ff4253cd62bf3e7d07414287a603a5c48d77305b8d86eb6
    sig1_hex = '9f2f2061e1898665c6ae49e665bc5f344a6005104c242d53f74c8548de7a468502ac0b1b2e9be9f26ff4253cd62bf3e7d07414287a603a5c48d77305b8d86eb6'
    # sha1(bill)
    m_hash2 = 'c692d6a10598e0a801576fdd4ecf3c37e45bfbc4'
    # nc chal.cybersecurityrumble.de 10101
    # bill
    # Your token: bill,9f2f2061e1898665c6ae49e665bc5f344a6005104c242d53f74c8548de7a4685c5bdd8fb22a1aa7035c6f9788ec7e58598c343f8f3d5f7325f6b869cb2d84215
    sig2_hex = '9f2f2061e1898665c6ae49e665bc5f344a6005104c242d53f74c8548de7a4685c5bdd8fb22a1aa7035c6f9788ec7e58598c343f8f3d5f7325f6b869cb2d84215'

    m_hash1 = int(m_hash1, 16)
    r = int(sig1_hex[:len(sig1_hex)//2], 16)
    sig1 = int(sig1_hex[len(sig1_hex)//2:], 16)
    m_hash2 = int(m_hash2, 16)
    sig2 = int(sig2_hex[len(sig2_hex)//2:], 16)

    print("m_hash1 = " + hex(m_hash1))
    print("sig1 = " + hex(sig1))
    print("m_hash2 = " + hex(m_hash2))
    print("sig2 = " + hex(sig2))
    print("r = " + hex(r))

    r_i = inverse_mod(r, curve.order)
    m_h_diff = (m_hash1 - m_hash2) % curve.order

    for k_try in (sig1 - sig2, sig1 + sig2, -sig1 - sig2, -sig1 + sig2):

        k = (m_h_diff * inverse_mod(k_try, curve.order)) % curve.order

        s_E = (((((sig1 * k) % curve.order) - m_hash1) % curve.order) * r_i) % curve.order

        key = SigningKey.from_secret_exponent(s_E, curve=curve, hashfunc=hash_algorithm)

        if key.get_verifying_key().pubkey.verifies(m_hash1, Signature(r, sig1)):
            print("ECDSA Private Key = " + "".join("{:02x}".format(c) for c in key.to_string())) # If we got here we found a solution
            return key

def sign_text(priv_key):
    sk = ecdsa.SigningKey.from_string(priv_key.to_string(), curve=curve)
    vk = sk.get_verifying_key()
    sig = sk.sign(text_to_sign)
    signed_message = "".join("{:02x}".format(c) for c in sig)
    return "{},{}".format(text_to_sign.decode("utf-8"), signed_message)

def send_message(s_m):
    target = remote('chal.cybersecurityrumble.de', 10100)
    print("Sending '{}'".format(s_m))
    target.sendline(s_m)
    target.interactive()

signed_message = sign_text(get_key_from_hash())
print(send_message(signed_message))