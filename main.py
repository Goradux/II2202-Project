import cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import time
from sys import getsizeof
import random
import os
import string


##
# AES example
def aes_example(string):

    start = time.time()
    key = os.urandom(32)
    iv = os.urandom(16)
    print(round(time.time() - start, 3))
    # CBC initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(b"a secret message") + encryptor.finalize()
    print(round(time.time() - start, 3))
    # print(ct)
    # print(getsizeof(ct))
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    end = time.time()
    # print(decrypted_message)
    # print(getsizeof(decrypted_message))
    print(round(end - start, 5))
##


def test_aes(msg: str) -> int:
    # implement the algorithm here
    key = os.urandom(16)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)
def test_blowfish(msg: str) -> int:
    # implement the algorithm here
    key = os.urandom(16)
    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)
    # return getsizeof(msg)
def test_rsa(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)
def test_elliptic(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)
def test_idea(msg: str) -> int:
    # implement the algorithm here
    key = os.urandom(16)
    iv = os.urandom(8)
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)
    # return getsizeof(msg)
def test_tripledes(msg: str) -> int:
    # implement the algorithm here
    key = os.urandom(16)
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)
    # return getsizeof(msg)


algos = [
    ['AES', test_aes],
    ['Blowfish', test_blowfish],
    ['RSA', test_rsa],
    ['elliptic curve', test_elliptic],
    ['IDEA', test_idea],
    ['tripleDES', test_tripledes],
]


messages = [
    ['very short', ''.join(random.choice(string.ascii_letters) for i in range(16))],    
    ['short', ''.join(random.choice(string.ascii_letters) for i in range(64))],    
    ['medium', ''.join(random.choice(string.ascii_letters) for i in range(256))],    
    ['long', ''.join(random.choice(string.ascii_letters) for i in range(1024))],
    ['very long', ''.join(random.choice(string.ascii_letters) for i in range(4096))],
]


def main():
    for index, algo in enumerate(algos):
        for msg in messages:
            print('Testing:', algo[0], 'with a', msg[0], 'message')
            # run it once, so no time overhead for initilization
            algo[1](msg[1])

            start = time.time()
            
            # this is where we are calling the encryption algorithm
            for _ in range(1000):
            #     when run 1000 times on my PC takes around 8 ms for AES
                payload = algo[1](msg[1])
            # mb needs to be run multiple times if a single one is too fast. Like 100 times?

            end = time.time()
            print('Total execution time:', round(end - start, 6), 'seconds')
            print('Total payload size:', payload, 'bytes')
            print()
        print('--------------------------')

if __name__ == "__main__":
    main()
    # for _ in range(10):
    #     aes_example()
    # print(messages)