import math
from typing import Sequence
from primes.primes_utils import check_prime, prime_list
import unittest
import primes
import functools as ft
import itertools as it

class TestPrimeSieve(unittest.TestCase):
    def setUp(self) -> None:
        self.TEST_UPTO = 10**3
        self.ps = primes.PrimeSieve(self.TEST_UPTO)
    
    def test_smallest_prime_factor_works_for_n_leq_size(self):
        for n in range(2, self.TEST_UPTO+1):
            ps = primes.PrimeSieve(n)
            try:
                #this should not raise any exceptions
                a = ps.smallest_prime_factor((2+n)//2)
                b = ps.smallest_prime_factor(n) #edge case
                self.assertIsInstance(a, int, msg="smallest prime factor should be an int")
                self.assertIsInstance(b, int, msg="smallest prime factor should be an int")

            except:
                raise Exception("prime sieve shouldn't raise an exception on input <= size")
    
    def test_smallest_prime_factor_works_for_n_leq_size_squared(self):
        for n in range(self.TEST_UPTO+1, min(self.TEST_UPTO**2 + 1, self.TEST_UPTO*2), 3):
            a = self.ps.smallest_prime_factor(n) # this should not raise an exception
            self.assertIsInstance(a, int, msg="smallest prime factor should be an int")

    def test_smallest_prime_factor_fails_on_too_large_inputs(self):
        self.assertRaises(Exception, self.ps.smallest_prime_factor, self.TEST_UPTO**2 + 1, msg="smallest_prime_factor should fail on input > size^2")

    def test_smallest_prime_factor_is_a_factor_leq_size(self):
        for n in range(2, self.TEST_UPTO):
            self.assertTrue(n % self.ps.smallest_prime_factor(n) == 0)

    def test_smallest_prime_factor_is_a_factor_leq_size_squared(self):
        for n in range(self.TEST_UPTO, min(self.TEST_UPTO**2 + 1, self.TEST_UPTO*2)):
            self.assertTrue(n % self.ps.smallest_prime_factor(n) == 0)


class TestPrimeFactoriztions(unittest.TestCase):
    def setUp(self):
        self.TEST_UPTO = 10**3
        self.ps = primes.PrimeSieve(self.TEST_UPTO)


    def test_prime_factors_generator_types(self):
        for n in range(2, self.TEST_UPTO):
            for t in primes.prime_factors_generator(n, self.ps):
                self.assertIsInstance(t, tuple, msg="generator must yield tuples")
                self.assertEqual(len(t), 2, msg="yielded tuple must consist of two elements")
                self.assertIsInstance(t[0], int, msg="factor must be an int")
                self.assertIsInstance(t[1], int, msg="power of a factor must be an int")
                self.assertGreaterEqual(t[1], 1, msg="power of a factor must be >= 1")
    
    def test_prime_factors_generator_yields_only_prime_factors(self):
        for n in range(2, self.TEST_UPTO):
            prev = 0
            for t in primes.prime_factors_generator(n, self.ps):
                self.assertGreater(t[0], prev, msg="factors must be yielded in an increasing order")
                self.assertTrue(primes.check_prime(t[0], self.ps), msg="factors must be primes")
    
    def sum_factor_powers(self, factors : Sequence[tuple[int, int]]) -> int:
        return ft.reduce(lambda acc, x: acc + x[1], factors, 0)

    def test_get_prime_factors_correct_sum_of_factor_powers_for_primes(self):
        for p in prime_list(self.ps, upto=self.TEST_UPTO):
            factors = primes.prime_factors_generator(p, prime_sieve=self.ps)
            self.assertEqual(self.sum_factor_powers(factors), 1, msg="\n for n = {}".format(p))

    def test_get_prime_factors_correct_sum_of_factor_powers_for_composites(self):
        sq = math.isqrt(self.TEST_UPTO)
        for a in range(2, sq+1):
            for b in range(a, sq+1):
                n = a*b
                factors = primes.prime_factors_generator(n, prime_sieve=self.ps)            
                self.assertGreater(self.sum_factor_powers(factors), 1, msg="if number is not prime its factorization should have sum of factor powers > 1")

    def sum_factorizations(self, facA: Sequence[tuple[int, int]], facB: Sequence[tuple[int, int]]) -> Sequence[tuple[int, int]]:
        res = []
        i, j = 0, 0
        while i < len(facA) and j < len(facB):
            if facA[i][0] == facB[j][0]: # same prime occurs in both
                res.append((facA[i][0], facA[i][1] + facB[j][1]))
                i += 1
                j += 1
            elif facA[i][0] < facB[i][0]:
                res.append(facA[i])
            else:
                res.append(facB[i])
        return res

    def test_get_prime_factors_number_factors_add_on_multiplication(self):
        sq = math.floor(self.TEST_UPTO**(1/4))
        for a in range(2, sq+1, 5):
            for b in range(a, sq+1, 5):
                factors_a = primes.get_prime_factors(a, self.ps)
                factors_b = primes.get_prime_factors(b, self.ps)
                factors_product = primes.get_prime_factors(a*b, prime_sieve=self.ps)            
                self.assertEqual(self.sum_factorizations(factors_a, factors_b), factors_product)


    def test_get_prime_factors_reversible_to_original(self):
        def revert_factorization(factors):
            return ft.reduce(lambda acc, x: acc * (x[0]**x[1]), factors, 1)
        
        for n in range(2, self.TEST_UPTO):
            self.assertEqual(n, revert_factorization(primes.get_prime_factors(n, prime_sieve=self.ps)), msg="reverting factorization must ")
    

class TestPrimeUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.ps = primes.PrimeSieve(10000)
        self.first_100_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
    
    def all_prime(self, nums : Sequence[int]) -> bool:
        return all(map(primes.check_prime, nums, it.repeat(self.ps)))

    def test_check_prime(self):
        self.assertTrue(self.all_prime(self.first_100_primes), msg="check prime must be true for primes")
        for a in range(2,50):
            for b in range(a, 50):
                self.assertFalse(check_prime(a*b, self.ps), msg="check prime must be false for composite numbers")

    def test_prime_list(self):
        for n in range(2,1000, 17):
            lst = primes.prime_list(self.ps, upto=n)
            self.assertTrue(self.all_prime(lst), msg="all numbers generated by prime_list must be prime")

    def test_nth_prime(self):
        self.assertEqual(list(map(primes.nth_prime, range(1,51), it.repeat(self.ps))), primes.prime_list(self.ps, n=50))


if __name__ == "__main__":
    unittest.main()
