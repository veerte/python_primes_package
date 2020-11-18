import unittest
import math

import primes
import primes.pi_computations as PC

class TestS(unittest.TestCase):
    def setUp(self) -> None:
        self.N = 10**3
        self.ps = primes.PrimeSieve(self.N)
    
    def test_S_equal_S_brute_force(self):
        pl = primes.prime_list(prime_sieve=self.ps, upto=math.isqrt(self.N))
        for k in range(0,4):
            self.assertEqual(PC.S(self.N, k, pl), PC.S_brute_force(self.N, k, pl), msg="n={}, k={}".format(self.N, k)) 

class TestLegendreSum(unittest.TestCase):
    def setUp(self) -> None:
        self.N = 10**3
        self.ps = primes.PrimeSieve(self.N)
    
    def test_equal_to_brute_force(self):
        pl_sqr = primes.prime_list(prime_sieve=self.ps, upto=math.isqrt(self.N))
        pl = primes.prime_list(prime_sieve=self.ps, upto=self.N)
        self.assertTrue(True)
        
class TestPiComputationMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.N = 10**5
        self.test_values = ((1,0), (10,4), (100,25), (1000, 168), (10000, 1229), (100000, 9592))

    def test_pi_from_list(self):
        ps = primes.PrimeSieve(self.N)
        for n, correct_val in self.test_values:
            res = PC.pi_from_list(n, prime_list=primes.prime_list(prime_sieve=ps, upto=n))
            self.assertEqual(res, correct_val)

    def test_pi_meissel(self):
        for n, correct_val in self.test_values:
            res = PC.pi_meissel(n)
            self.assertEqual(res, correct_val)

    def test_pi_lucy_hedgehog(self):
        for n, correct_val in self.test_values:
            self.assertEqual(PC.pi_lucy_hedgehog(n), correct_val, msg="failed on input {}".format(n))

if __name__ == "__main__":
    unittest.main()