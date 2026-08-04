import os
import pytest
import time
import threading
from crew_ai.training_loop import update_strategy, reset_cache, _yaml_to_dict

TEST_FILEPATH = "crew_ai/test_learned_strategies_temp.yaml"

@pytest.fixture(autouse=True)
def cleanup():
    """Ensures test clean state before and after each test."""
    reset_cache()
    if os.path.exists(TEST_FILEPATH):
        os.remove(TEST_FILEPATH)
    yield
    reset_cache()
    if os.path.exists(TEST_FILEPATH):
        os.remove(TEST_FILEPATH)

def test_update_strategy_calculation():
    """
    Verifies that the strategy metrics (total trades, success rate, and efficiency)
    are calculated correctly.
    """
    # 1. First trade: success=True, volume=10.0
    res1 = update_strategy(success=True, volume=10.0, force_flush=True, filepath=TEST_FILEPATH)
    assert res1["total_trades"] == 1
    assert res1["success_rate"] == 1.0
    assert res1["efficiency_score"] == 15.0  # 10.0 * 1.5 = 15.0

    # 2. Second trade: success=False, volume=20.0
    res2 = update_strategy(success=False, volume=20.0, force_flush=True, filepath=TEST_FILEPATH)
    assert res2["total_trades"] == 2
    assert res2["success_rate"] == 0.5  # (1.0 + 0.0) / 2 = 0.5
    assert res2["efficiency_score"] == 12.5  # (15.0 + (20.0 * 0.5)) / 2 = (15.0 + 10.0) / 2 = 12.5

def test_update_strategy_batching_and_flushing():
    """
    Verifies that disk I/O only occurs when force_flush=True or when batch_limit is reached.
    """
    # Verify no file exists initially
    assert not os.path.exists(TEST_FILEPATH)

    # Update without flushing (batch_limit is 5)
    for _ in range(4):
        update_strategy(success=True, volume=1.0, force_flush=False, batch_limit=5, filepath=TEST_FILEPATH)

    # File should not be created on disk yet
    assert not os.path.exists(TEST_FILEPATH)

    # 5th update should trigger auto-flush
    update_strategy(success=True, volume=1.0, force_flush=False, batch_limit=5, filepath=TEST_FILEPATH)
    assert os.path.exists(TEST_FILEPATH)

    # Verify content parsed from file matches cached expectation
    disk_data = _yaml_to_dict(open(TEST_FILEPATH).read())
    assert disk_data["total_trades"] == 5

def test_update_strategy_concurrency():
    """
    Verifies that update_strategy is thread-safe and calculates correct values
    even when called concurrently from multiple threads.
    """
    threads = []
    num_threads = 10
    updates_per_thread = 15

    def worker():
        for _ in range(updates_per_thread):
            update_strategy(success=True, volume=1.0, force_flush=False, batch_limit=500, filepath=TEST_FILEPATH)

    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Flush manually at the end and get final stats
    final_res = update_strategy(success=True, volume=1.0, force_flush=True, filepath=TEST_FILEPATH)

    # We started with num_threads * updates_per_thread + 1 (the final force_flush)
    expected_total = num_threads * updates_per_thread + 1
    assert final_res["total_trades"] == expected_total

def test_update_strategy_performance_gain():
    """
    Benchmarks the performance of batched (buffered) I/O versus unbuffered disk writes.
    Expected to show a dramatic speedup (often 50x-100x+).
    """
    iterations = 50

    # Benchmark Unbuffered (flushes on every iteration)
    reset_cache()
    if os.path.exists(TEST_FILEPATH):
        os.remove(TEST_FILEPATH)

    start_unbuffered = time.perf_counter()
    for _ in range(iterations):
        update_strategy(success=True, volume=2.0, force_flush=True, filepath=TEST_FILEPATH)
    unbuffered_duration = time.perf_counter() - start_unbuffered

    # Benchmark Buffered (only flushes once at the end)
    reset_cache()
    if os.path.exists(TEST_FILEPATH):
        os.remove(TEST_FILEPATH)

    start_buffered = time.perf_counter()
    for i in range(iterations):
        # Only flush on the last iteration
        is_last = (i == iterations - 1)
        update_strategy(success=True, volume=2.0, force_flush=is_last, batch_limit=iterations + 10, filepath=TEST_FILEPATH)
    buffered_duration = time.perf_counter() - start_buffered

    # Ensure the final result is correctly written to disk
    assert os.path.exists(TEST_FILEPATH)
    disk_data = _yaml_to_dict(open(TEST_FILEPATH).read())
    assert disk_data["total_trades"] == iterations

    speedup = unbuffered_duration / (buffered_duration if buffered_duration > 0 else 1e-9)
    print(f"\nUnbuffered (direct disk writes): {unbuffered_duration:.6f}s")
    print(f"Buffered (in-memory caching): {buffered_duration:.6f}s")
    print(f"Speedup ratio: {speedup:.1f}x faster")

    # Assert that caching provides at least a 5x performance improvement
    assert speedup > 5
