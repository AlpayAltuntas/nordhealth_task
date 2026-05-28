"""
equal_sum_pairs.py
==================
Find and print all unique pairs in an unsorted array that share the same sum.

Algorithm
---------
1. Generate all unique index-pairs (i, j) with i < j  →  O(n²)
2. Group pairs by their sum using a dict[int, list[tuple]]  →  O(1) per insert
3. Emit every sum that has ≥ 2 distinct pairs  →  O(output)

Overall time complexity : O(n²)
Overall space complexity : O(n²)  (at most n*(n-1)/2 pairs stored)

Python API
----------
    from equal_sum_pairs import find_equal_sum

    result = find_equal_sum([6, 4, 12, 10, 22, 54, 32, 42, 21, 11])
    # {16: [(6, 10), (4, 12)], 32: [(10, 22), (21, 11)], ...}

    result = find_equal_sum([6, 4, 12, 10, 22, 54, 32, 42, 21, 11], formatted=True)
    # "Pairs : ( 6, 10) ( 4, 12) have sum : 16\\n..."

CLI
---
    python equal_sum_pairs.py 6 4 12 10 22 54 32 42 21 11
    python equal_sum_pairs.py 6 4 12 10 22 54 32 42 21 11 --json
    python equal_sum_pairs.py          # runs built-in examples
    python equal_sum_pairs.py --help
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import combinations
from typing import Generator, Union


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

Pair = tuple[int, int]


def _generate_pairs(array: list[int]) -> Generator[tuple[int, Pair], None, None]:
    """
    Yield (sum, (a, b)) for every unique pair in *array*.

    Using itertools.combinations keeps indices implicit and guarantees
    each pair is emitted exactly once without needing seen-set bookkeeping.
    """
    for a, b in combinations(array, 2):
        yield a + b, (a, b)


def find_equal_sum_pairs(array: list[int]) -> dict[int, list[Pair]]:
    """
    Return a mapping of  sum  →  list-of-pairs  where the sum is shared
    by at least two distinct pairs.

    Parameters
    ----------
    array:
        Input integers (need not be sorted or unique).

    Returns
    -------
    dict mapping each shared sum to the list of (a, b) pairs that produce it,
    ordered by the position of *a* in the original array.
    """
    if len(array) < 4:
        # We need at least 4 elements to form 2 distinct pairs.
        return {}

    sum_map: dict[int, list[Pair]] = defaultdict(list)
    for s, pair in _generate_pairs(array):
        sum_map[s].append(pair)

    # Keep only sums that have 2+ pairs, preserving original encounter order.
    return {s: pairs for s, pairs in sum_map.items() if len(pairs) >= 2}


def find_equal_sum(
    array: list[int],
    formatted: bool = False,
) -> Union[dict[int, list[Pair]], str]:
    """
    Public entry point — find all unique pairs that share the same sum.

    Parameters
    ----------
    array:
        Input integers (need not be sorted or unique).
    formatted:
        If True, return a print-ready string instead of the raw dict.

    Returns
    -------
    dict  (formatted=False, default)
        ``{sum: [(a, b), ...], ...}`` — only sums shared by ≥ 2 pairs.
    str   (formatted=True)
        Canonical "Pairs : … have sum : …" output, one line per sum.

    Examples
    --------
    >>> find_equal_sum([6, 4, 12, 10, 22, 54, 32, 42, 21, 11])
    {16: [(6, 10), (4, 12)], ...}

    >>> print(find_equal_sum([6, 4, 12, 10], formatted=True))
    Pairs : ( 6, 10) ( 4, 12) have sum : 16
    """
    results = find_equal_sum_pairs(array)
    return format_results(results) if formatted else results




def _format_pair(pair: Pair) -> str:
    return f"( {pair[0]}, {pair[1]})"


def format_results(results: dict[int, list[Pair]]) -> str:
    """Render the results dict into the canonical output string."""
    lines: list[str] = []
    for s, pairs in sorted(results.items()):          # stable: sort by sum
        pairs_str = " ".join(_format_pair(p) for p in pairs)
        lines.append(f"Pairs : {pairs_str} have sum : {s}")
    return "\n".join(lines)


def print_results(array: list[int]) -> None:
    """High-level helper: run the algorithm and print to stdout."""
    results = find_equal_sum_pairs(array)
    if not results:
        print("No pairs with equal sums found.")
        return
    print(format_results(results))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_numbers(tokens: list[str]) -> list[int]:
    """
    Convert CLI tokens to a list of ints, supporting two separator styles:

    - Comma-separated  →  ``1,2,3,4``  or  ``1, 2, 3, 4``  (commas present)
    - Space-separated  →  ``1 2 3 4``                       (no commas)

    When commas are present the joined token string is split on commas so that
    both ``1,2,3`` (single token) and ``1, 2, 3`` (multiple tokens) work
    identically.  Raises ``SystemExit`` with a clear message on bad input.
    """
    joined = " ".join(tokens)

    if "," in joined:
        parts = [p.strip() for p in joined.split(",") if p.strip()]
    else:
        parts = joined.split()

    try:
        return [int(p) for p in parts]
    except ValueError as exc:
        sys.exit(f"Error: all values must be integers — {exc}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="equal_sum_pairs",
        description="Find all unique pairs in an array that share the same sum.",
        epilog=(
            "Input formats accepted:\n"
            "  Space-separated : 1 2 3 4 5\n"
            "  Comma-separated : 1,2,3,4,5\n"
            "  Comma + spaces  : 1, 2, 3, 4, 5\n"
            "Omit numbers entirely to run the built-in examples."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "numbers",
        nargs="*",
        type=str,           # raw strings — _parse_numbers handles conversion
        metavar="N",
        help="integers to analyse",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="output results as JSON instead of plain text",
    )
    return parser


DEFAULT_EXAMPLES: list[tuple[str, list[int]]] = [
    (
        "A[] = { 6, 4, 12, 10, 22, 54, 32, 42, 21, 11 }",
        [6, 4, 12, 10, 22, 54, 32, 42, 21, 11],
    ),
    (
        "A[] = { 4, 23, 65, 67, 24, 12, 86 }",
        [4, 23, 65, 67, 24, 12, 86],
    ),
]


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.numbers:
        numbers = _parse_numbers(args.numbers)
        _run_and_print(numbers, as_json=args.json)
        return

    # No numbers supplied → run the problem-statement defaults
    for label, arr in DEFAULT_EXAMPLES:
        print(f"Input:  {label}")
        print("Output:")
        _run_and_print(arr, as_json=args.json)
        print()


def _run_and_print(array: list[int], *, as_json: bool = False) -> None:
    """Compute and print results for *array* in either plain-text or JSON format."""
    results = find_equal_sum(array)

    if not results:
        msg = {"message": "No pairs with equal sums found."} if as_json else "No pairs with equal sums found."
        print(json.dumps(msg) if as_json else msg)
        return

    if as_json:
        # JSON: {sum: [[a, b], ...], ...} — sorted by sum for determinism
        payload = {str(s): list(map(list, pairs)) for s, pairs in sorted(results.items())}
        print(json.dumps(payload, indent=2))
    else:
        print(format_results(results))


if __name__ == "__main__":
    main()