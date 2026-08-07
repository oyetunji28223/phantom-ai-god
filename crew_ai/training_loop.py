import os
import threading

# BOLT OPTIMIZATION: In-memory caching and batched/buffered disk I/O for strategy updates.
# Constantly writing strategy updates directly to the filesystem (unbuffered YAML writes)
# introduces a massive I/O bottleneck, which severely slows down agent training loops.
# This implementation reads the strategy YAML file exactly once to populate an in-memory cache,
# buffers subsequent updates in memory, and only flushes to disk periodically (after batch_limit
# updates) or when explicitly requested via `force_flush=True`.
# This implementation is fully thread-safe, utilizing a threading lock to synchronize
# concurrent updates to global caches.

# Map filepaths to their respective in-memory cache dictionaries: {filepath: strategy_dict}
_strategy_cache = {}
# Map filepaths to their pending update counts: {filepath: int}
_pending_updates_count = {}

# Re-entrant Lock to secure the global caches in concurrent environments
_lock = threading.RLock()

DEFAULT_STRATEGY = {
    "total_trades": 0,
    "success_rate": 0.0,
    "efficiency_score": 0.0,
}

def _dict_to_yaml(data: dict) -> str:
    """Serializes a flat dictionary into simple YAML format."""
    lines = []
    for k, v in sorted(data.items()):
        lines.append(f"{k}: {v}")
    return "\n".join(lines) + "\n"

def _yaml_to_dict(yaml_str: str) -> dict:
    """Parses a simple flat YAML format string into a dictionary."""
    data = {}
    for line in yaml_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            # Try to cast values to appropriate numeric types
            try:
                if "." in v:
                    data[k] = float(v)
                else:
                    data[k] = int(v)
            except ValueError:
                data[k] = v
    return data

def reset_cache() -> None:
    """Resets the in-memory cache and pending updates counts (mainly for testing)."""
    global _strategy_cache, _pending_updates_count
    with _lock:
        _strategy_cache.clear()
        _pending_updates_count.clear()

def update_strategy(
    success: bool,
    volume: float,
    force_flush: bool = False,
    batch_limit: int = 100,
    filepath: str = "crew_ai/learned_strategies.yaml"
) -> dict:
    """
    Updates the learning strategy based on trade success and volume.
    Utilizes an in-memory cache to prevent redundant disk I/O.
    This function is thread-safe.

    Args:
        success (bool): Whether the simulated trade was successful.
        volume (float): The trading volume.
        force_flush (bool): If True, flushes updates to disk immediately.
        batch_limit (int): Flush changes to disk after this many pending updates.
        filepath (str): The YAML file path.

    Returns:
        dict: A copy of the updated strategy parameters.
    """
    global _strategy_cache, _pending_updates_count

    # Normalize the filepath to avoid key mismatches
    normalized_path = os.path.abspath(filepath)

    with _lock:
        # 1. Load the strategy parameters if they are not cached for this file
        if normalized_path not in _strategy_cache:
            if os.path.exists(normalized_path):
                try:
                    with open(normalized_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        _strategy_cache[normalized_path] = _yaml_to_dict(content)
                except Exception:
                    _strategy_cache[normalized_path] = DEFAULT_STRATEGY.copy()
            else:
                _strategy_cache[normalized_path] = DEFAULT_STRATEGY.copy()

            # Ensure all default keys are present in cache
            for k, v in DEFAULT_STRATEGY.items():
                if k not in _strategy_cache[normalized_path]:
                    _strategy_cache[normalized_path][k] = v

        cache = _strategy_cache[normalized_path]

        # 2. Update the strategy parameters (simulating an incremental learning calculation)
        old_trades = cache["total_trades"]
        new_trades = old_trades + 1

        old_success_rate = cache["success_rate"]
        new_success_rate = (old_success_rate * old_trades + (1.0 if success else 0.0)) / new_trades

        # Metric computation representing learning update
        # Better trades with higher volume yield a higher efficiency score
        trade_reward = volume * (1.5 if success else 0.5)
        old_efficiency = cache["efficiency_score"]
        new_efficiency = (old_efficiency * old_trades + trade_reward) / new_trades

        cache["total_trades"] = new_trades
        cache["success_rate"] = round(new_success_rate, 4)
        cache["efficiency_score"] = round(new_efficiency, 4)

        # Increment pending updates buffer for this file
        _pending_updates_count[normalized_path] = _pending_updates_count.get(normalized_path, 0) + 1

        # 3. Flush to disk if batch limit is reached or force_flush is set
        if _pending_updates_count[normalized_path] >= batch_limit or force_flush:
            yaml_content = _dict_to_yaml(cache)
            # Ensure target directory exists
            os.makedirs(os.path.dirname(normalized_path), exist_ok=True)
            with open(normalized_path, "w", encoding="utf-8") as f:
                f.write(yaml_content)
            _pending_updates_count[normalized_path] = 0

        # Return a copy to avoid mutation of the internal cached state outside of the lock
        return cache.copy()
