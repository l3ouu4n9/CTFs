from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
import base64
from secret import flag

RECEIVER_NUM = 7

def generate_safecurve():
    while True:
        p = random_prime(2 ^ 256-1, False, 2 ^ 255)
        a = randint(-p, p)
        b = randint(-p, p)

        if 4*a^3 + 27*b^2 == 0:
            continue

        E = EllipticCurve(GF(p), [a, b])

        fac = list(factor(E.order()))

        # Prevent rho method
        if fac[-1][0] < 1 << 80:
            continue

        # Prevent transfer
        for k in range(1, 20):
            if (p ^ k - 1) % fac[-1][0] == 0:
                break
        else:
            return E

class Sender:
    def __init__(self, curves, receivers):
        self.secret = randint(1 << 254, 1 << 255)
        self.curves = curves
        self.receivers = receivers
        self.shared_secrets = [None for _ in range(len(receivers))]

    def setup_connections(self):
        for idx, receiver in enumerate(self.receivers):
            curve = self.curves[idx]
            print(f"curves[{idx}] : {curve}")
            g = self.curves[idx].gens()[0]
            print(f"g[{idx}] = {g.xy()}")
            receiver.set_curve(curve, g)
            public = self.secret * g
            print(f"S_pub[{idx}] = {public.xy()}")
            yours = receiver.key_exchange(public)
            print(f"R_pub[{idx}] = {yours.xy()}")
            self.shared_secrets[idx] = yours * self.secret

    def send_secret(self):
        msg = b'Hi, here is your flag: ' + flag
        for idx, receiver in enumerate(self.receivers):
            px = self.shared_secrets[idx].xy()[0]
            _hash = sha256(long_to_bytes(px)).digest()
            key = _hash[:16]
            iv = _hash[16:]
            encrypted_msg = base64.b64encode(AES.new(key, AES.MODE_CBC, iv).encrypt(pad(msg, 16)))
            print(f"encrypted_msg[{idx}] = {encrypted_msg}")
            receiver.receive(encrypted_msg)


class Receiver:
    def __init__(self):
        self.secret = randint(1 << 254, 1 << 255)
        self.curve = None
        self.g = None
        self.shared_secret = None

    def set_curve(self, curve, g):
        self.curve = curve
        self.g = g

    def key_exchange(self, yours):
        self.shared_secret = yours * self.secret
        return self.g * self.secret

    def receive(self, encrypted_msg):
        px = self.shared_secret.xy()[0]
        _hash = sha256(long_to_bytes(px)).digest()
        key = _hash[:16]
        iv = _hash[16:]
        msg = AES.new(key, AES.MODE_CBC, iv).decrypt(base64.b64decode(encrypted_msg))
        msg = unpad(msg, 16)
        assert msg.startswith(b'Hi, here is your flag: ')


receivers = [Receiver() for _ in range(RECEIVER_NUM)]
curves = [generate_safecurve() for _ in range(RECEIVER_NUM)]

A = Sender(curves, receivers)
A.setup_connections()
A.send_secret()
