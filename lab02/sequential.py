import numpy as np
import sys


def find_primes(high: int):

    numbers = np.arange(high + 1, dtype=int)
    mask = np.ones_like(numbers, dtype=bool)
    mask[0:2] = False
    for i in range(2, int(np.sqrt(high)) + 1):
        if mask[i]:
            mask[i*i::i] = False
    
    return numbers[mask]


def find_primes_interval(low: int, high: int, dividers: list):
    
    numbers = np.arange(low, high + 1, dtype=int)
    mask = np.ones_like(numbers, dtype=bool)
    for n in numbers:
        i = n - low
        for d in dividers:
            if n % d == 0:
                mask[i] = False
                break
    
    return numbers[mask]


def find_primes_parallel(high: int):

    limit_B = int(np.sqrt(high))
    dividers_B = find_primes(limit_B)
    primes_C = find_primes_interval(limit_B + 1, high, dividers_B)
    primes = np.concatenate((dividers_B, primes_C))

    return primes
    

if __name__ == "__main__":
    
    assert len(sys.argv) == 2, "Programm requires one argument - an upper limit of the prime"

    high = int(sys.argv[1])
    primes_parallel = find_primes_parallel(high)
    primes = find_primes(high)

    assert np.array_equal(primes, primes_parallel), "Primes are not equal"

    print(f"There are {len(primes_parallel)} primes up to {high}:\n{primes_parallel}")
