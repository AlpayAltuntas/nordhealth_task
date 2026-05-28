# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

WORKDIR /app

# Install dependencies in a separate layer so they are cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY equal_sum_pairs.py .

# ── Test stage ─────────────────────────────────────────────────────────────────
FROM base AS test

COPY test_equal_sum_pairs.py .

# Run the full test suite (with coverage) as part of the image build
RUN pytest test_equal_sum_pairs.py -v --cov=equal_sum_pairs --cov-report=term-missing

# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM base AS runtime

ENTRYPOINT ["python", "equal_sum_pairs.py"]
# Default: no args → runs the built-in problem-statement examples
# Override: docker run equal-sum-pairs 6 4 12 10 22