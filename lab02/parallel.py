#!/usr/bin/env python

import mpi4py
import numpy as np
import sys

from mpi4py import MPI


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

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    limit_B = int(np.sqrt(high))
    dividers_B = find_primes(limit_B)
    primes = np.copy(dividers_B)

    if rank == 0:
        # Calculate the interval length
        n_workers = size - 1
        interval_length = int(np.ceil((high - limit_B) / n_workers))

        # Send intervals to worker processes
        low_i = limit_B + 1
        high_i = limit_B + interval_length
        for i in range(1, n_workers):
            comm.send(low_i, dest=i)
            comm.send(high_i, dest=i)
            low_i += interval_length
            high_i += interval_length
        comm.send(low_i, dest=n_workers)
        comm.send(high, dest=n_workers)
    else:
        # Worker process
        low = comm.recv(source=0)
        high = comm.recv(source=0)

        primes_C = find_primes_interval(low, high, dividers_B)
        comm.send(primes_C, dest=0)

    if rank == 0:
        # Master process
        for i in range(1, size):
            primes_C = comm.recv(source=i)
            primes = np.concatenate((primes, primes_C))

        # Print the primes
        print(f"There are {len(primes)} primes up to {high}:\n{np.sort(primes)}")

    MPI.Finalize()


if __name__ == "__main__":
    high = int(sys.argv[1])
    find_primes_parallel(high)
