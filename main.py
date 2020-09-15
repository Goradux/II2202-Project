import cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import time
from sys import getsizeof
import random
import os
import string
from datetime import datetime
from glob import glob


##
# AES example  MINIMIZE THIS
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

##
# RSA example  MINIMIZE THIS
def rsa_example():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    message = b"encrypted data encrypted data encrypted data encrypted data encrypted data encrypted data encrypted data encrypted data encrypted data encrypted data encrypted data encrypted data encrypted " # for some reason 207 is the limit that the current key_size will allow
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    if plaintext == message:
        print(True)
    print(ciphertext)
    print(getsizeof(ciphertext))
    print(plaintext, message)
    print(getsizeof(message))

##


def test_aes(msg: str) -> int:
    key = os.urandom(16)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)
def test_blowfish(msg: str) -> int:
    key = os.urandom(16)
    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)
def test_rsa(msg: str) -> int:
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
    new_msgs = []
    # partition the msg if it is too long for the key_size
    if len(msg) > 128:
        for i in range(round(len(msg)/128)):
            new_msgs.append(msg[(128*i):(128*i+128)])

    if new_msgs == []:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,  # according to this: https://www.ibm.com/support/knowledgecenter/SSLTBW_2.4.0/com.ibm.zos.v2r4.icha700/keysizec.htm
                            # 512 - low sec, 1024 - medium sec, 2048 - high sec, 4096 - very high sec
        )
        public_key = private_key.public_key()
        message = bytes(msg, 'utf-8')
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return getsizeof(ciphertext)
    else:
        total_size = 0
        for part in new_msgs:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            public_key = private_key.public_key()
            message = bytes(part, 'utf-8')
            ciphertext = public_key.encrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            total_size += getsizeof(ciphertext)
        return total_size
# def test_elliptic(msg: str) -> int:
    # implement the algorithm here
    # return getsizeof(msg)
def test_idea(msg: str) -> int:
    key = os.urandom(16)
    iv = os.urandom(8)
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)
def test_tripledes(msg: str) -> int:
    key = os.urandom(16)
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(msg, 'utf-8')) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ct) + decryptor.finalize()
    return getsizeof(ct)


algos = [
    ['AES', test_aes],
    ['Blowfish', test_blowfish],
    # ['elliptic curve', test_elliptic],
    # ['IDEA', test_idea],
    ['tripleDES', test_tripledes],
    ['RSA', test_rsa],
]


messages = [
    ['very-short', ''.join(random.choice(string.ascii_letters) for i in range(16))],    
    ['short', ''.join(random.choice(string.ascii_letters) for i in range(64))],    
    ['medium', ''.join(random.choice(string.ascii_letters) for i in range(256))],    
    ['long', ''.join(random.choice(string.ascii_letters) for i in range(1024))],
    ['very-long', ''.join(random.choice(string.ascii_letters) for i in range(4096))],
]


def main():
    for index, algo in enumerate(algos):
        for msg in messages:
            print('Testing:', algo[0], 'with a', msg[0], 'message')
            # run it once, so no time overhead for initilization
            algo[1](msg[1])

            log_name = datetime.now().strftime('%Y-%m-%d_%H-%M.txt')
            with open('./data/{}_{}_{}'.format(algo[0], msg[0], log_name), 'a') as log:
                pass

            
            repeats = 0
            # RSA takes a lot longer to test, so run only 5 instances
            if algo[0] == 'RSA':
                repeats = 5
            else:
                repeats = 1000    
                
            first_start = time.time()

            # this is where we are calling the encryption algorithm
            for _ in range(repeats):
                start = time.time()
                payload = algo[1](msg[1])
                end = time.time()
                with open('./data/{}_{}_{}'.format(algo[0], msg[0], log_name), 'a') as log:
                    log.write(str((end - start)*1000) + '\n')
            # mb needs to be run multiple times if a single one is too fast. Like 100 times?

            end = time.time()

            

            print('Total execution time (per 1 instance):', round((end - first_start)/repeats*1000, 3), 'ms')
            print('Total payload size:', payload, 'bytes')
            print()
        print('--------------------------')

if __name__ == "__main__":
    files = glob('./data/*')
    for f in files:
        os.remove(f)
    main()
    # start = time.time()
    # time.sleep(1)
    # print(time.time() - start)
