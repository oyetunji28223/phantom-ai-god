import time
from crew_ai.planner import evaluate_token

def test_evaluate_token_correctness():
    # Verify outputs are deterministic
    btc_score1 = evaluate_token("BTC")
    btc_score2 = evaluate_token("BTC")
    assert btc_score1 == btc_score2
    assert 1 <= btc_score1 <= 100

    # Check invalid inputs return 0
    assert evaluate_token("") == 0
    assert evaluate_token(None) == 0

def test_evaluate_token_caching_speedup():
    # Warm up / cache values
    evaluate_token("SOL")
    evaluate_token("ETH")
    evaluate_token("BTC")

    # First timed run with cached values (should be virtually instantaneous)
    start_time = time.perf_counter()
    for _ in range(10000):
        evaluate_token("SOL")
        evaluate_token("ETH")
        evaluate_token("BTC")
    duration = time.perf_counter() - start_time

    # Assert that 30,000 requests complete extremely fast (under 100ms) thanks to caching
    assert duration < 0.1, f"Expected cache lookup to be extremely fast, but took {duration:.6f}s"
