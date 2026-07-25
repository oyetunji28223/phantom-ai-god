import pytest
import time
from crew_ai.planner import evaluate_token

def test_evaluate_token_returns_consistent_score():
    """
    Verifies that evaluate_token returns consistent scores for the same token.
    """
    score1 = evaluate_token("BTC")
    score2 = evaluate_token("BTC")
    assert 1 <= score1 <= 100
    assert score1 == score2

def test_evaluate_token_cache_behavior():
    """
    Verifies that the LRU cache is working correctly and prevents redundant calls.
    """
    # Clear cache to ensure clean statistics for the test
    evaluate_token.cache_clear()

    # First evaluation: cache miss
    score_sol = evaluate_token("SOL")
    info = evaluate_token.cache_info()
    assert info.hits == 0
    assert info.misses == 1

    # Second evaluation: cache hit (no computation)
    score_sol_2 = evaluate_token("SOL")
    assert score_sol == score_sol_2
    info = evaluate_token.cache_info()
    assert info.hits == 1
    assert info.misses == 1

def test_evaluate_token_performance_gain():
    """
    Measures and asserts the performance improvement of using caching.
    The first call (cache miss) should be measurably slower than the cached call (cache hit).
    """
    evaluate_token.cache_clear()

    # Measure uncached (cache miss)
    start_time = time.perf_counter()
    evaluate_token("ETH")
    uncached_duration = time.perf_counter() - start_time

    # Measure cached (cache hit)
    start_time = time.perf_counter()
    evaluate_token("ETH")
    cached_duration = time.perf_counter() - start_time

    # Assert that the cached call is significantly faster (at least 10x speedup)
    speedup = uncached_duration / (cached_duration if cached_duration > 0 else 1e-9)
    print(f"\nUncached: {uncached_duration:.6f}s, Cached: {cached_duration:.6f}s, Speedup: {speedup:.1f}x")
    assert speedup > 10
