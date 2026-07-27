import time
import hashlib
from functools import lru_cache

# Let's define an uncached version and a cached version for direct comparison
def evaluate_token_uncached(token_name: str) -> int:
    if not token_name or not isinstance(token_name, str):
        return 0
    # Simulate some deterministic computation
    hash_val = int(hashlib.md5(token_name.encode('utf-8')).hexdigest(), 16)
    score = (hash_val % 100) + 1
    return score

@lru_cache(maxsize=1024)
def evaluate_token_cached(token_name: str) -> int:
    return evaluate_token_uncached(token_name)

def run_benchmark():
    print("Starting token evaluation benchmark...")

    # Simulating repeated requests for token evaluations during an optimization/planning cycle
    tokens = ["BTC", "ETH", "SOL", "ADA", "DOT", "LINK", "UNI", "DOGE"] * 50000

    # Timing uncached
    start_time = time.perf_counter()
    results_uncached = [evaluate_token_uncached(token) for token in tokens]
    duration_uncached = time.perf_counter() - start_time

    # Timing cached (pre-warmed because of lru_cache)
    start_time_cached = time.perf_counter()
    results_cached = [evaluate_token_cached(token) for token in tokens]
    duration_cached = time.perf_counter() - start_time_cached

    print(f"Total tokens processed: {len(tokens)}")
    print(f"Uncached run duration: {duration_uncached:.6f} seconds")
    print(f"Cached run duration:   {duration_cached:.6f} seconds")

    if duration_cached > 0:
        speedup = duration_uncached / duration_cached
        print(f"Estimated Cache Speedup factor: {speedup:.2f}x")
    else:
        print("Cached run was too fast to measure speedup accurately!")

if __name__ == "__main__":
    run_benchmark()
