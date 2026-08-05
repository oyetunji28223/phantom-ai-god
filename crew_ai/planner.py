from functools import lru_cache
import math

def _heavy_token_calculation(token_name: str) -> int:
    """
    Performs a heavy, CPU-bound calculation to evaluate the risk/utility score
    of a token based on its character weights, primes, and geometric sequences.
    """
    if not token_name:
        return 0

    score = 0
    # Simulate realistic string analysis (complexity, frequency, and custom hashes)
    for i, char in enumerate(token_name):
        char_val = ord(char)
        # Some expensive math functions
        score += int(math.sin(char_val) * (i + 1) * 100)

        # Fibonacci / sequence calculations
        a, b = 0, 1
        for _ in range(min(char_val % 30, 20)):
            a, b = b, a + b
        score += a

    # Ensure standard scoring range [1, 1000]
    final_score = int(abs(score) % 1000) + 1
    return final_score

@lru_cache(maxsize=1024)
def evaluate_token(token_name: str) -> int:
    """
    Evaluates the token score using cache to optimize performance
    for repetitive lookups.
    """
    # Optimized: caches expensive token character / math evaluations.
    return _heavy_token_calculation(token_name)
