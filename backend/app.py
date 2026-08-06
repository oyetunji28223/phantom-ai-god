import time
from crew_ai.planner import evaluate_token

def run_backend_simulation():
    """
    Simulates the backend engine processing token data feed.
    Utilizes the cached evaluate_token to maintain low latency.
    """
    print("Starting Phantom AI Backend Simulation...")
    # Simulated stream of incoming tokens to evaluate
    tokens = ["BTC", "ETH", "SOL", "PHANTOM", "GODMODE"] * 50
    start = time.perf_counter()
    for token in tokens:
        _ = evaluate_token(token)
    duration = time.perf_counter() - start
    print(f"Backend processed {len(tokens)} token events in {duration:.6f} seconds.")

if __name__ == "__main__":
    run_backend_simulation()
