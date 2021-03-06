import itertools as it
import math

from .primeSieve import PrimeSieve

# very very low quality, needs improvement
def next_prime_brute(n : int, prime_sieve : PrimeSieve) -> int:
    if n == 1:
        return 2
    
    if n % 2 == 0:
        n += 1

    while not check_prime(n, prime_sieve):
        n += 2
    
    return n

def next_prime(n: int, prime_sieve: PrimeSieve) -> int:
    """Returns the smallest prime greater than `from`"""
    return next_prime_brute(n, prime_sieve)

def check_prime(num : int, prime_sieve : PrimeSieve) -> bool:
    if num < 0:
        raise Exception("Checking primality of number below 0")
    if num <= 1:
        return False
    if num <= prime_sieve.size**2:
        return prime_sieve.smallest_prime_factor(num) == num
    else:
        raise Exception("Number larger than sieve size squared, can't check for primality")


    

def prime_list(prime_sieve : PrimeSieve, *, upto : int = None, n : int = None):
    """
    Returns a list of primes p <= upto if 'upto' keyword argument is supplied,
    or the list of first n primes if 'n' keyword argument is supplied.
    Precisely one of 'upto' and 'n' keyword args must be supplied, otherwise an error is raised.
    """
    if not ((upto is None) ^ (n is None)):
        raise Exception("precisely one of upto or n keyword arguments must be supplied")

    prime_list = []

    if upto:
        if upto >= 2:
            prime_list.append(2)
        for i in range(3, upto+1, 2):
            if check_prime(i, prime_sieve):
                prime_list.append(i)
    else:
        if n >= 1:
            prime_list.append(2)
        
        i = 3
        while len(prime_list) < n:
            if check_prime(i, prime_sieve):
                prime_list.append(i)
            i += 2
    
    return prime_list

# rolling sieve
def psieve():
    yield from (2, 3, 5, 7)
    sieve_dict = {}
    ps = psieve()
    next(ps)        # drop the initial 2 from the helper psieve
    p = next(ps)    # p = 3
    psq = p*p  
    for c in it.count(9, 2):  # start from 3^2, skip all evens
        if c in sieve_dict:      # means that c is composite - WHY?
            step = sieve_dict.pop(c)
        elif c < psq:   # prime
            yield c
            continue
        else:           # composite, = p*p
            assert c == psq
            step = 2*p
            p = next(ps)
            psq = p*p
        
        c += step
        while c in sieve_dict:
            c += step
        sieve_dict[c] = step


def nth_prime(n : int, prime_sieve : PrimeSieve) -> int:
    """Returns the nth prime. SUPER SLOW"""
    if n == 1:
        return 2
    
    i = 1
    for d in it.count(3, step=2):
        if not check_prime(d, prime_sieve):
            continue
        i += 1
        if i == n:
            return d

