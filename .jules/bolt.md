# Bolt's Journal

## 2026-07-26 - [No PyYAML library in default Python environment]
**Learning:** The Python environment does not contain the third-party `yaml` (PyYAML) library by default. Attempting to import it results in a ModuleNotFoundError. However, because YAML is simple and human-readable, flat YAML configurations/state can be easily parsed and serialized using pure-Python standard library string manipulations.
**Action:** Use standard library string/file manipulation or simple custom parser/formatter functions to serialize and deserialize flat YAML files to avoid adding external dependencies.
