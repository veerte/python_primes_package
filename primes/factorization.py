from typing import Iterator
from .primeSieve import PrimeSieve
from .primes_utils import check_prime
import math
from collections.abc import Iterable
import itertools as it


def get_prime_factors(num : int, prime_sieve : PrimeSieve = None) -> list[tuple[int, int]]:
    if prime_sieve is not None:
        return list(prime_factors_generator(num, prime_sieve))
    else:    
        return get_prime_factorization_no_sieve(num)


def prime_factors_generator(num : int, prime_sieve : PrimeSieve) -> Iterator[tuple[int, int]]:
    x = num

    # if x is > prime_sieve.size this loop will try to bring it below the size
    # by finding small primes and dividing by them
    for d in it.chain([2], it.count(3, step=2)):
        if x <= prime_sieve.size:
            break

        if not check_prime(d, prime_sieve) or x % d != 0:
            continue
        
        factor_power = 0
        while x % d == 0:
            x = x//d
            factor_power += 1
        yield (d, factor_power)


    spf = prime_sieve.smallest_prime_factor(x) # will be larger than any of the factors yielded before
    while x > 1:
        factor_prime = spf
        factor_power = 0

        while spf == factor_prime:
            x = x//factor_prime
            factor_power += 1
            spf = prime_sieve.smallest_prime_factor(x)
        
        yield (factor_prime, factor_power)

# O(sqrt(n))
def get_prime_factorization_no_sieve(num : int) -> list[tuple[int, int]]:
    if (num < 2):
        return []
    initial = num
    pf = []
    cnt = 0
    for d in [2]:
        cnt = 0
        while num % d == 0:
            num = num//d
            cnt += 1
        if cnt > 0:
            pf.append((d,cnt))

    for d in range(3, math.floor(math.sqrt(num))+1, 2):
        cnt = 0
        while num % d == 0:
            num = num//d
            cnt += 1
        if cnt > 0:
            pf.append((d,cnt))
    if num != 1:
        pf.append((num, 1))
    return pf
