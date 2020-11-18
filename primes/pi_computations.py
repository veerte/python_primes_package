from bisect import bisect
from typing import Sequence
import functools as ft
import itertools as it
import operator
import typing
import math

from .primeSieve import PrimeSieve
from .primes_utils import prime_list, next_prime 

T = typing.TypeVar('T')

def product(nums : Sequence[T]) -> T:
    return ft.reduce(operator.mul, nums, 1)

def S(N : int, k : int, prime_list : list[int]) -> int:
    """Number of positive integers <= N that are divisible by any combination of k primes from the list"""
    return sum(map(lambda comb: N//product(comb), it.combinations(prime_list, k)))

def S_brute_force(N : int, k : int, prime_list : list[int]) -> int:
    total = 0
    for comb in it.combinations(prime_list, k):
        prod = product(comb)
        for x in range(1, N+1):
            if x % prod == 0:
                total += 1
    return total


def legendre_sum(N : int, a : int, prime_list : list[int]) -> int:
    """
    Returns the total number of positive integers x <= N that are not divisible by any of the first a primes

    Args:
        N: the number positive integers to check up to.
        a: consider only the first a primes.
        prime_list: list of primes; must contain at least a elements
    
    Returns:
        the total number of positive integers x such that x <= N and x is not divisible by any of the first a primes
    """
    assert(a <= len(prime_list))
    total = 0
    sign = 1
    i = 0
    e = S(N, i, prime_list[:a])
    while e > 0 and i <= a:
        total += sign * e
        i += 1
        sign = -sign
        e = S(N, i, prime_list[:a])
    return total

def pi_legendre(N : int, _prime_sieve : PrimeSieve = None) -> int:
    """
    Computes the value of the pi function at N using legendre's formula

    Args:
        N: the argument for which to compute the value of the pi function
        prime_sieve: a sufficiently large sieve to be used in computation
    Returns:
        The int value of the pi function at N
    """
    sqrtN = math.isqrt(N)

    if _prime_sieve is None:
        _prime_sieve = PrimeSieve(sqrtN)

    pl = prime_list(_prime_sieve, upto=sqrtN)
    a = pi_from_list(sqrtN, pl)
    return a + legendre_sum(N, a, pl) - 1

def pi_brute(N : int):
    ps = PrimeSieve(N)
    return len(prime_list(ps, upto=N))

def pi_from_list(x : int, prime_list : list[int]) -> int:
    return bisect(prime_list, x)

def P(k : int, N : int, a : int, _prime_sieve : PrimeSieve, _prime_list : list[int]) -> int:
    """
    The number of positive integers <=N which can be written as products of precisely k primes p_i where i>a.
    """
    if k == 1:
        # in this case the only numbers that can be written as a product of one prime
        # with index > a are the primes > a, and there's pi(N) - a of them
        # but this should not really be called directly
        #return pi_from_list(N, prime_sieve) - a
        return 0

    if k == 2:
        b = pi_generic(math.isqrt(N), _prime_sieve, _prime_list) # p_b is the largest prime <= sqrt(N)
        if a >= b:
            return 0 #because p_b is the last prime <=sqrt(N), so a>=b implies p_{a+1} > sqrt(N) so p{a+1}*p{j>=(a+1)} > N 
        
        pn = (b - a) * (b + a - 1) // 2
        s = sum(map(lambda i: pi_generic(N//_prime_list[i-1], _prime_sieve, _prime_list), range(a+1, b+1)))
        return s - pn
    
    raise Exception("P_k is not implemented for k != 2")

def pi_meissel(N : int, _prime_sieve : PrimeSieve = None, _prime_list : list[int] = None) -> int:
    #print("call to pi_meissel with N={}".format(N))
    
    if N == 1:
        return 0
    
    sqrtN = math.isqrt(N)
    cbrtN = math.floor(N**(1/3))
    
    # create sieve and prime list if they are not supplied by a previous iteration
    if _prime_sieve is None:
        _prime_sieve = PrimeSieve(sqrtN)
    if _prime_list is None:
        _prime_list = prime_list(_prime_sieve, upto=sqrtN)

    c = pi_generic(cbrtN, _prime_sieve, _prime_list) #p_c is the largest prime <= cbrtN

    lgsum = legendre_sum(N, c, _prime_list)

    p2 = P(2, N, c, _prime_sieve, _prime_list)

    return lgsum - p2 + c - 1

pi_cache = {1: 0}
def pi_generic(N : int, _prime_sieve : PrimeSieve = None, _prime_list : list[int] = None) -> int:
    if N in pi_cache:
        return pi_cache[N]
    
    if _prime_list is not None and N <= _prime_list[-1]:
        return pi_from_list(N, _prime_list)
    else:
        return pi_meissel(N, _prime_sieve, _prime_list)

def pi_lucy_hedgehog(N: int) -> int:
    r = math.isqrt(N)
    div_results = [N // v for v in range(1, r)]
    V = div_results + list(range(r, 0, -1))
    
    T = lambda x: x - 1
    S = {v: T(v) for v in V}

    for p in range(2,r+1):
        if S[p] > S[p-1]:  # number of primes changed, so p must be a prime
            for v in it.takewhile(lambda v: v >= p*p, V):
                # nprap - number of new primes removed while sieving range [2..v] with p
                # == number of primes in range [p..v//p]
                nprap = S[v//p] - S[p-1]
                S[v] -= nprap
    return S[N]

if __name__ == "__main__":

    print(pi_lucy_hedgehog(10**7))
    # print(pi_generic(10**5))

