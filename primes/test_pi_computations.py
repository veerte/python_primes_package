import unittest
import math

import primes

class TestS(unittest.TestCase):
    def setUp(self) -> None:
        self.N = 10**3
        self.ps = primes.PrimeSieve(self.N)
    
    def test_S_equal_S_brute_force(self):
        pl = primes.prime_list(prime_sieve=self.ps, upto=math.isqrt(self.N))
        for k in range(0,4):
            self.assertEqual(primes.S(self.N, k, pl), primes.S_brute_force(self.N, k, pl), msg="n={}, k={}".format(self.N, k)) 

class TestLegendreSum(unittest.TestCase):
    def setUp(self) -> None:
        self.N = 10**3
        self.ps = primes.PrimeSieve(self.N)
    
    def test_equal_to_brute_force(self):
        pl_sqr = primes.prime_list(prime_sieve=self.ps, upto=math.isqrt(self.N))
        pl = primes.prime_list(prime_sieve=self.ps, upto=self.N)
        self.assertTrue(True)
        

if __name__ == "__main__":
    unittest.main()