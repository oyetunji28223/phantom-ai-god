import time
from crew_ai.planner import evaluate_token

def test_evaluate_token_correctness():
    # Test valid input returns expected score ranges [1, 100]
    score_btc = evaluate_token("BTC")
    score_eth = evaluate_token("ETH")
    assert 1 <= score_btc <= 100
    assert 1 <= score_eth <= 100

    # Test invalid inputs
    assert evaluate_token(None) == 0
    assert evaluate_token("") == 0
    assert evaluate_token(123) == 0

    # Test determinism
    assert evaluate_token("SOL") == evaluate_token("SOL")

def test_evaluate_token_caching_and_performance():
    # Clear the cache before testing caching metrics
    evaluate_token.cache_clear()

    initial_info = evaluate_token.cache_info()
    assert initial_info.hits == 0
    assert initial_info.misses == 0

    # First call (miss)
    evaluate_token("DOGE")
    info_after_first = evaluate_token.cache_info()
    assert info_after_first.misses == 1
    assert info_after_first.hits == 0

    # Second call (hit)
    evaluate_token("DOGE")
    info_after_second = evaluate_token.cache_info()
    assert info_after_second.misses == 1
    assert info_after_second.hits == 1

    # Benchmark CPU hash calculation vs cached lookup
    # Generate distinct tokens for a cold run to ensure we are testing real performance
    distinct_tokens = [f"TOKEN_{i}" for i in range(1000)]

    # 1. Cold execution (all cache misses)
    start_cold = time.perf_counter()
    for token in distinct_tokens:
        evaluate_token(token)
    time_cold = time.perf_counter() - start_cold

    # 2. Warm execution (all cache hits)
    start_warm = time.perf_counter()
    for token in distinct_tokens:
        evaluate_token(token)
    time_warm = time.perf_counter() - start_warm

    # Cache hit should be orders of magnitude faster
    speedup = time_cold / max(time_warm, 1e-9)
    print(f"\nCold evaluation (cache misses) of 1000 tokens took: {time_cold:.6f} seconds")
    print(f"Warm evaluation (cache hits) of 1000 tokens took: {time_warm:.6f} seconds")
    print(f"Calculated speedup factor: {speedup:.2f}x")

    assert speedup > 2.0, f"Expected speedup of at least 2.0x, but got {speedup:.2f}x"
