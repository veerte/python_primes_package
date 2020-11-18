
from primes import is_prime

def prime_sequence_length(a, b):
    n = 0
    def y(n):
        return n*n + a*n + b
    while is_prime(y(n)):
        n+=1
    return n

curr_max = 0
curr_pair = (0,2)
for a in range(-1000,1000):
    for b in range(-1000,1000):
        res = prime_sequence_length(a,b)
        if res > curr_max:
            curr_max = res
            curr_pair = (a,b)

print(curr_pair, curr_max)
print(curr_pair[0] * curr_pair[1]) 