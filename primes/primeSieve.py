import math

class PrimeSieve:
    """
    Allows to check the smallest prime factor of all numbers not exceeding sieve size
    """
    def __init__ (self, size : int, verbose : bool = False):
        self.size = size
        self.verbose = verbose

        self.sieve = self.make_sieve(upto=size)
        self.list = [2,3]
        self.list_upto = 3

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
        if x >= len(self.sieve):
            raise Exception("Number larger than sieve size")
        a = self.sieve[x]
        return x if a == 0 else a

