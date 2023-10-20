from collections import Counter
from typing import Iterator

from .prime_generator import PrimeGenerator
from primegenerators.algorithms import binary_search2, binary_search


# noinspection SpellCheckingInspection
class EratosthenesGenerator(PrimeGenerator):
    """
    Prime number generator using the Sieve of Eratosthenes
    """

    _primes = []

    def _uncached_primes(self) -> Iterator[int]:
        """
        Generate an infinite series of primegenerators, starting from the first
        prime not in the cache.
        :return:
        """
        current_value = 1 if not self._primes else self._primes[-1]
        while True:
            is_prime = True

            current_value += 2

            for factor in self._primes:
                if not current_value % factor:
                    is_prime = False
                    break

                if factor * factor > current_value:
                    break

            if is_prime:
                if not self._primes or self._primes[-1] < current_value:
                    self._primes.append(current_value)

                yield current_value

    def primes(self) -> Iterator[int]:
        """
        Generate an endless series of prime numbers, starting with 2.

        :return: An iterator over the series of prime numbers.
        """

        yield 2

        # Run through the cache
        for prime in self._primes:
            yield prime

        yield from self._uncached_primes()

    def primes_range(self, minimum: int, maximum: int) -> Iterator[int]:
        """
        Return an iterator over the series of prime numbers between minimum
        and maximum inclusive.

        :param minimum:
        :param maximum:
        :return:
        """

        for p in self.primes():
            if p > maximum:
                break

            if p >= minimum:
                yield p

    def is_prime(self, candidate: int) -> bool:
        """
        Determine whether a given number is prime or not.

        :param candidate: The number to be checked for prime-ness
        :return: True if the candidate number is prime, otherwise False
        """

        if candidate < 2 or candidate % 2 == 0:
            return False

        # If the number is in the cache, it must be prime
        # if candidate in self._primes:
        if binary_search(self._primes, candidate) >= 0:
            return True

        for factor in self.primes():
            if candidate % factor == 0:
                return candidate == factor

            if factor * factor >= candidate:
                break

        return True

    def prime_factors(self, number: int) -> Counter:
        """
        Calculate the prime factors of a number.

        :param number: The number to be factorized
        :return: A Counter object containing the prime factors of number
        """

        factors = []

        for factor in self.primes():
            while number % factor == 0:
                factors.append(factor)
                number //= factor
            if number == 1:
                break

        return Counter(factors)
