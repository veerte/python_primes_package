import math

class PrimeSieve:
    """
    Allows to check the smallest prime factor of all numbers not exceeding sieve size
    """
    def __init__ (self, size : int, verbose : bool = False):
        self.verbose = verbose
        self.size = size
        self.sieve = self.make_sieve(upto=size)

    def make_sieve(self, upto : int) -> list:
        """
        Creates a list L such that L[x] is the biggest prime factor of x or 0 if x is a prime 
        """
        sieve = [0] * (upto + 1)
        for d in range(2, math.isqrt(upto) + 1):
            if sieve[d]:
                continue

            for d_mult in range(2*d, upto+1, d):
                if not sieve[d_mult]:
                    sieve[d_mult] = d
        return sieve 

    def smallest_prime_factor(self, x : int) -> int:
        if x < 0:
            raise Exception("Negative number was supplied")
        if x <= 1:
            return x
        if x <= self.size:
            a = self.sieve[x]
            return x if a == 0 else a

        if x <= self.size**2:
            for p in range(2, math.isqrt(x)+1):
                if self.sieve[p]:
                    continue # skip all composite numbers
                if x % p == 0:
                    return p
            # if nothing was returned by now it means that no prime <=sqrt(x) divides x,
            # therefore x is prime and is the smallest prime factor of itself
            return x
        
        else:
            raise Exception("Number greater than sieve size squared")

        