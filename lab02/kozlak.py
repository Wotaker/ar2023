from mpi4py import MPI
import math
import sys

def sieve_eratosthenes_parallel(comm, n):
    rank = comm.Get_rank()
    size = comm.Get_size()

    local_size = n // size
    start = rank * local_size + 2
    end = (rank + 1) * local_size + 2 if rank != size - 1 else n

    max_B = int(math.sqrt(n)) + 1
    B = [True] * max_B
    B[0], B[1] = False, False
    B_divisors = []

    # pierwszy krok - znalezienie podzielników w przedziale B
    for i in range(len(B)):
        if B[i]:
            prime = i
            B_divisors.append(prime)
            while (prime < max_B):
                if B[prime]:
                    B[prime] = False
                prime *= 2

    # print(B_divisors)

    primes_in_range = []
    if start == 2:
        primes_in_range += B_divisors
    for i in range(start, end):
        flag = True
        for divisor in B_divisors:
            if (i % divisor == 0) and i:
                flag = False
                break
        if flag:
            primes_in_range.append(i)

    return primes_in_range

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Podaj N - gorna granice przedzialu")
        exit(0)
    else:
        n = int(sys.argv[1])

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print('size=%d, rank=%d' % (size, rank))

    primes = sieve_eratosthenes_parallel(comm, n)

    primes_combined = comm.gather(primes, root=0)

    if rank == 0:
        print(primes_combined)


    # probe(2, 0)
    # probe(2,1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
