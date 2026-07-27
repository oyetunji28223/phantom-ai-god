# Bolt's Journal - Critical Learnings Only

## 2025-08-04 - Caching Token Evaluation in CrewAI Planner
**Learning:** Evaluated tokens are frequently queried during agent planning sessions. Standardizing token evaluation with high-performance `lru_cache` provides a significant reduction in duplicate computation overhead and simulation latency.
**Action:** Use `functools.lru_cache(maxsize=1024)` on critical deterministic evaluation pathways to optimize performance.
