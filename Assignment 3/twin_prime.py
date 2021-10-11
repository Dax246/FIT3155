"""
Assignment 3 Question 1 FIT3155
Author: Damien Ambegoda 30594235
"""
import random
import sys


def modular_exponential(base, mod, num):
    """ Finds the answer to base**num mod (mod)

    :return: base ** num mod (mod)
    """
    # Removes 0b from the front of binary representation
    binary_representation = bin(num)[2:]
    values = [(base ** 2 ** 0) % mod]
    for index in range(1, len(binary_representation)):
        values.append((values[-1]) ** 2 % mod)

    res = 1
    for i in range(len(binary_representation) - 1, -1, -1):
        if binary_representation[len(binary_representation) - i - 1] == "1":
            res = (res * values[i]) % mod

    return res


# Based off pseudocode from 3155 Lectures
def millerRabins(n, k):
    """ Determines if n is prime (or most likely prime)

    :param n: number to check for primality
    :param k: accuracy
    :return: 1 if probably prime, 0 if composite
    """
    if n % 2 == 0:
        return 0
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t = t//2
    for _ in range(k):
        a = random.randrange(2, n-1)
        repeated_squaring = [modular_exponential(a, n, t)]
        for i in range(1, s + 1):
            next_in_sequence = (repeated_squaring[-1]) ** 2 % n
            if next_in_sequence == 1:
                if repeated_squaring[-1] != 1 and repeated_squaring[-1] != n-1:
                    # Composite so return 0
                    return 0
            repeated_squaring.append(next_in_sequence)

    if repeated_squaring[-1] != 1:
        # Composite so return 0
        return 0
    # Probably prime so return 1
    return 1

def twin_prime(m):
    """ Determines a twin prime in the range [2^{m -1} , 2^m -1]

    :param m: bits required to represent the twin primes
    :return: the pair of twin primes
    """
    k = 64
    shift = 0

    # This helps set the lower bound for the random number where the lower bound must be divisible by 6
    while (2**(m-1) + shift) % 6 != 0:
        shift += 1

    # Checked number is a dictionary containing all the random numbers that were already checked before
    # A dictionary on average has O(1) lookup but can be O(n) in its worst case.
    # The benefit of not running miller rabins on a number already checked most likely outweighs the detriment of having
    # to use a dictionary to store and search for numbers already used
    checked_numbers = {}
    while True:
        # This gets a random number that is divisible by 6 with the use of the modified lower bound
        randnum = random.randrange(2**(m-1) + shift, 2 ** m, 6) - 1
        if randnum in checked_numbers:
            continue
        checked_numbers[randnum] = 0
        prime = millerRabins(randnum, k)
        if prime:
            if millerRabins(randnum + 2, k):
                return randnum, randnum + 2



if __name__ == '__main__':
    m = sys.argv[1]
    output = twin_prime(int(m))
    f = open("output_twin_prime.txt", "w")
    f.write(str(output[0]) + "\n")
    f.write(str(output[1]))
    f.close()