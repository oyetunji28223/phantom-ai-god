# Bolt's Performance Journal

This journal records critical performance learnings specific to the Phantom AI Godmode codebase.

## 2026-07-31 - Caching Deterministic Calculations
**Learning:** Repetitive execution of heavy CPU-bound cryptographic hash evaluations for tokens introduces unnecessary overhead in the trading loop. Since these calculations are deterministic based on the token symbol, they are perfect candidates for caching.
**Action:** Use `functools.lru_cache` to memoize the results of `evaluate_token` and avoid redundant hash calculations.

## 2026-07-31 - Batched Disk I/O & Zero-Dependency Parsing
**Learning:** Continuously updating and rewriting strategy states directly to the filesystem on every simulated trade introduces a severe disk I/O bottleneck. Additionally, the sandbox environment lacks standard third-party YAML parser libraries (like PyYAML), which can lead to import failures or heavy overhead.
**Action:** Implement an in-memory caching mechanism with batched disk writing (flushing after a batch limit or when forced). Write pure-Python lightweight YAML serialization and deserialization helpers to avoid dependency overhead and environmental errors.
