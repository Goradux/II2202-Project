import cryptography
import time
from sys import getsizeof

def test_aes(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)
def test_blowfish(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)
def test_rsa(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)
def test_elliptic(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)
def test_idea(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)
def test_tripledes(msg: str) -> int:
    # implement the algorithm here
    return getsizeof(msg)


algos = [
    ['AES', test_aes],
    ['Blowfish', test_blowfish],
    ['RSA', test_rsa],
    ['elliptic curve', test_elliptic],
    ['IDEA', test_idea],
    ['tripleDES', test_tripledes],
]


def main():
    for index, algo in enumerate(algos):
        print('Testing:', algo[0])
        start = time.time()
        payload = algo[1]('something')
        end = time.time()
        print('Total execution time:', round(end - start, 3), 'seconds')
        print('Total payload size:', payload, 'bytes')
        print()

if __name__ == "__main__":
    main()