# Bolt's Performance Journal

## 2026-08-04 - PyYAML Dependency Constraint on Python Runtime
**Learning:** The default Python environment in this repository does not have the `yaml` (PyYAML) package installed. Importing `yaml` directly causes `ModuleNotFoundError` during pytest execution. To achieve safe, zero-dependency caching of learning updates, flat dictionaries must be serialized and deserialized using lightweight, pure-Python YAML helpers.
**Action:** Always write or use custom flat-YAML parse/serialize helpers in pure-Python instead of importing `yaml` or other third-party dependencies unless explicitly instructed or added.
