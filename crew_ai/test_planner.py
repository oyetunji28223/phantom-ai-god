import time
from crew_ai.planner import evaluate_token

def test_evaluate_token_known():
    # Test known tokens return expected computed scores
    btc_score = evaluate_token("BTC")
    eth_score = evaluate_token("ETH")
    sol_score = evaluate_token("SOL")

    assert btc_score > 100.0
    assert eth_score > 100.0
    assert sol_score > 100.0

def test_evaluate_token_fallback():
    # Test fallback compatibility to 100.0 for unknown tokens/inputs
    assert evaluate_token("UNKNOWN") == 100.0
    assert evaluate_token(None) == 100.0
    assert evaluate_token("") == 100.0

def test_evaluate_token_performance():
    # Clear cache before starting the benchmark
    evaluate_token.cache_clear()

    # 1. Measure uncached / original function performance (using the __wrapped__ function)
    start_time_uncached = time.perf_counter_ns()
    for _ in range(10000):
        _ = evaluate_token.__wrapped__("BTC")
        _ = evaluate_token.__wrapped__("ETH")
        _ = evaluate_token.__wrapped__("SOL")
    duration_uncached = time.perf_counter_ns() - start_time_uncached

    # 2. Measure cached function performance (using the decorated function)
    # First call will populate the cache (misses)
    evaluate_token("BTC")
    evaluate_token("ETH")
    evaluate_token("SOL")

    start_time_cached = time.perf_counter_ns()
    for _ in range(10000):
        _ = evaluate_token("BTC")
        _ = evaluate_token("ETH")
        _ = evaluate_token("SOL")
    duration_cached = time.perf_counter_ns() - start_time_cached

    # The cached execution should be significantly faster because it skips lookups and math
    print(f"\nUncached duration for 30k calls: {duration_uncached / 1_000_000:.2f} ms")
    print(f"Cached duration for 30k calls: {duration_cached / 1_000_000:.2f} ms")

    # Verify Cache Hits
    cache_info = evaluate_token.cache_info()
    assert cache_info.hits >= 30000

    # Assert cached is faster than uncached
    assert duration_cached < duration_uncached
