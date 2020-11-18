import math
import itertools as it
import functools as ft
import operator

from .primes_utils import check_prime, prime_list
from .primeSieve import PrimeSieve

def brute(N : int, sieve : PrimeSieve = None) -> int:
    """
    Computes the sum of prime list upto N
    """
    if sieve is None or sieve.size < N:
        sieve = PrimeSieve(N)
    
    return sum(prime_list(sieve, upto=N))

S_ref = {100: 1060, 50: 328, 33: 160, 25: 100, 20: 77, 16: 41, 14: 41, 12: 28, 11: 28, 10: 17, 9: 17, 8: 17, 7: 17, 6: 10, 5: 10, 4: 5, 3: 5, 2: 2, 1: 0}



def lucy_Hedgehog_method(N : int) -> int: #by Lucy_Hedgehog, https://projecteuler.net/thread=10;page=5
    r = math.isqrt(N)
    assert r*r <= N and (r+1)**2 > N # make sure r really is the integer square root of N

    div_results = [N//i for i in range(1,r+1)] # precomputed division results by factors <= intSqrt(N)  - O(n^0.5) int divisions
                                               # all of them will be >=isqrt(N), so >= r

    V = list(it.chain(div_results, range(r-1,0,-1)))

    assert V[r-1:] == list(range(r, 0, -1)) #the (r-1)th element is N//r = r by definition of integer square root
    assert all([V[i] > V[i+1] for i in range(0, len(V) - 2)]) # V is strictly decreasing

    # helper function
    def T(i : int) -> int:
        """returns sum of all integers upto i excluding '1' """
        return i*(i+1)//2-1

    S = {i : T(i) for i in V} 

    # values of S[1], S[2] and S[3] are always valid 
    # invariant: after the loop with p = k,
    # S[i] is the sum of all integers (except '1') not divisible by any of primes <= k
    # in particular, for i <= k^2 it is the sum of all primes <= i

    def invariant(k) -> bool:
        if N!=100:
            return True
        return all([S[i] == S_ref[i] for i in V if i <= k*k])

    # assume the initial state is after loop with p = 1.
    # k = 1, so S[1] must be valid
    assert invariant(k=1)

    # for all primes <= sqrt(N)
    for p in range(2,r+1):
        # we are guaranteed that p and p-1 are valid keys
        # because 2 <= p <= r, and all values from 1 to r are present in V
        
        # this checks if p is prime, because the invariant guarantees
        # that S[p] and S[p-1] are already the correct values, so
        # if the sum of primes <=p is greater than that <=(p-1)
        # it means p must be a prime 
        if S[p] > S[p-1]:  

            # for every value of v large enough that S(v, p)
            for v in it.takewhile(lambda v: v >= p*p, V):
                sk = S[v//p] - S[p-1] # sum of all k such that k only has divisors >= p, and k*p <= v
                                      # it would be 0 for v < p^2, because k*p >= p2 >= v, but  

                # sk * p is the sum of all numbers that get rejected precisely when p is used for sieving
                S[v] -= p*sk 
        else:
            pass
        
        # assert that invariant holds after the loop
        assert invariant(k=p)

    return S[N]

if __name__ == "__main__":
    N = 10**7
    print(lucy_Hedgehog_method(N))
    exit()

    ps = PrimeSieve(N)
    # time_func(1) (lambda N, ps: 2+sum(filter(ft.partial(check_prime, prime_sieve=ps), range(3, N+1, 2)))) (N, ps)
    # time_func(1) (lambda N, ps: 2+sum(filter(lambda x: check_prime(x, ps), range(3, N+1, 2)))) (N, ps)
    # time_func(1) (lambda N, ps: 2+sum([i for i in range(3,N+1,2) if check_prime(i, ps)])) (N, ps)
    a = time_func(1) (brute) (N, ps)
    print(a)
    print(time_func(1) (lucy_Hedgehog_method) (N))