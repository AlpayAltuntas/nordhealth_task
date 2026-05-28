# Equal Sum Pairs

Find all unique pairs in an unsorted array that share the same sum.

```
Input:  A[] = { 6, 4, 12, 10, 22, 54, 32, 42, 21, 11 }
Output:
Pairs : ( 6, 10) ( 4, 12) have sum : 16
Pairs : ( 10, 22) ( 21, 11) have sum : 32
...
```

## Algorithm

1. Generate all unique index-pairs `(i, j)` with `i < j` — **O(n²)**
2. Group pairs by their sum via a hash map — **O(1)** per insert
3. Emit every sum shared by ≥ 2 pairs

**Time:** O(n²) · **Space:** O(n²)

---

## Quick start

### Option A — Docker (recommended)

```bash
# Build and run with the built-in examples
make run

# Pass your own numbers (space-separated)
make run ARGS="6 4 12 10 22 54 32 42 21 11"

# JSON output
docker run --rm equal-sum-pairs 6 4 12 10 22 54 32 42 21 11 --json

# Run the full test suite
make test
```

### Option B — Local Python

```bash
pip install -r requirements-dev.txt

# Run with examples
python equal_sum_pairs.py

# Run with your own numbers
python equal_sum_pairs.py 6 4 12 10 22 54 32 42 21 11

# All input styles are equivalent:
python equal_sum_pairs.py 1 2 4 6 3 1          # space-separated
python equal_sum_pairs.py 1,2,4,6,3,1           # comma-separated
python equal_sum_pairs.py "1, 2, 4, 6, 3, 1"   # comma + spaces (quoted)
python equal_sum_pairs.py 1, 2, 4, 6, 3, 1      # comma + spaces (unquoted)

# JSON output
python equal_sum_pairs.py 6 4 12 10 22 54 --json

# Tests
make test-local

# Tests + coverage
make test-cov
```

### Option C — Python API

```python
from equal_sum_pairs import find_equal_sum

# Returns a dict: {sum: [(a, b), ...]}
result = find_equal_sum([6, 4, 12, 10, 22, 54, 32, 42, 21, 11])

# Returns a formatted string
output = find_equal_sum([6, 4, 12, 10, 22, 54, 32, 42, 21, 11], formatted=True)
print(output)
```

---

## Project structure

```
.
├── equal_sum_pairs.py       # Core algorithm + CLI
├── test_equal_sum_pairs.py  # 40 pytest tests
├── Dockerfile               # Multi-stage: base → test → runtime
├── docker-compose.yml       # app + test services
├── Makefile                 # build / run / test shortcuts
├── requirements.txt         # Runtime deps (stdlib only)
```

## Pylance / VS Code

If VS Code shows `Import "pytest" could not be resolved`, select the correct
interpreter:

1. **⌘ Shift P** → `Python: Select Interpreter`
2. Pick the environment where you ran `pip install -r requirements-dev.txt`
   (e.g. your Anaconda base or a project venv)
