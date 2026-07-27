from functools import lru_cache
import hashlib

@lru_cache(maxsize=1024)
def evaluate_token(token_name: str) -> int:
    """
    Evaluates a given token symbol/name to calculate its score or weight.
    Uses @lru_cache to optimize subsequent requests for identical token parameters.
    """
    if not token_name or not isinstance(token_name, str):
        return 0

    # Simulate a deterministic complex calculation using hashing
    hash_val = int(hashlib.md5(token_name.encode('utf-8')).hexdigest(), 16)
    score = (hash_val % 100) + 1
    return score
