import time
from crew_ai.planner import evaluate_token, _heavy_token_calculation

def test_evaluate_token_correctness():
    """
    Ensures that evaluate_token (cached) returns identical results to the un-cached calculation.
    """
    test_tokens = ["BTC", "ETH", "SOL", "PHANTOM_AI", "GODMODE", "", "A" * 100]
    for token in test_tokens:
        direct = _heavy_token_calculation(token)
        cached = evaluate_token(token)
        assert direct == cached, f"Mismatch for token {token}: {direct} != {cached}"

def test_evaluate_token_performance():
    """
    Benchmarks the cached version against the un-cached version.
    """
    tokens = ["BTC", "ETH", "SOL", "PHANTOM", "GODMODE", "AGENT", "BOLT", "SPEED"] * 200

    # Measure direct (un-cached) calls
    start_time = time.perf_counter()
    for token in tokens:
        _heavy_token_calculation(token)
    uncached_duration = time.perf_counter() - start_time

    # Measure cached calls
    start_time = time.perf_counter()
    for token in tokens:
        evaluate_token(token)
    cached_duration = time.perf_counter() - start_time

    print(f"\nUn-cached duration for {len(tokens)} calls: {uncached_duration:.6f}s")
    print(f"Cached duration for {len(tokens)} calls: {cached_duration:.6f}s")

    # Cached should be significantly faster
    assert cached_duration < uncached_duration
