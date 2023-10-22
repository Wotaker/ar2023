import numpy as np

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

    

if __name__ == "__main__":
    dividers_B = find_primes(10)
    primes_C = find_primes_interval(11, 100, dividers_B)

    primes = np.concatenate((dividers_B, primes_C))

    assert (primes == find_primes(100)).all(), "Something went wrong!"
