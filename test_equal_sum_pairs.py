"""
test_equal_sum_pairs.py
=======================
Comprehensive test suite for equal_sum_pairs.py

Run with:
    pytest test_equal_sum_pairs.py -v
"""

from __future__ import annotations
from pathlib import Path
import pytest

import json
import subprocess
import sys

from equal_sum_pairs import find_equal_sum, find_equal_sum_pairs, format_results, print_results, _parse_numbers
PROJECT_ROOT = Path(__file__).parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Not used in the tests, but can be helpful for debugging and writing new tests.
def result_as_set(results: dict) -> set:
    """
    Convert results to a frozenset of (sum, frozenset-of-pairs) so that
    tests are order-independent.
    """
    return {
        (s, frozenset(frozenset(p) for p in pairs))
        for s, pairs in results.items()
    }


# ---------------------------------------------------------------------------
# Core algorithm tests
# ---------------------------------------------------------------------------

class TestFindEqualSumPairs:

    def test_example_1(self):
        """Verify the first problem-statement example."""
        arr = [6, 4, 12, 10, 22, 54, 32, 42, 21, 11]
        results = find_equal_sum_pairs(arr)

        # Every reported sum must have ≥ 2 pairs.
        for s, pairs in results.items():
            assert len(pairs) >= 2, f"Sum {s} has fewer than 2 pairs"

        # Every pair must actually sum to the reported key.
        for s, pairs in results.items():
            for a, b in pairs:
                assert a + b == s, f"Pair ({a},{b}) does not sum to {s}"

        # Spot-check a known sum from the expected output.
        assert 16 in results
        assert (4, 12) in results[16] or (12, 4) in results[16]
        assert (6, 10) in results[16] or (10, 6) in results[16]

    def test_example_2(self):
        """Verify the second problem-statement example."""
        arr = [4, 23, 65, 67, 24, 12, 86]
        results = find_equal_sum_pairs(arr)

        assert 90 in results
        pairs_90 = {frozenset(p) for p in results[90]}
        assert frozenset({4, 86}) in pairs_90
        assert frozenset({23, 67}) in pairs_90

    def test_no_equal_sum_pairs(self):
        """Array where no two pairs share the same sum."""
        # [1, 2, 4, 8] — all pair sums are distinct: 3,5,9,6,10,12
        arr = [1, 2, 4, 8]
        assert find_equal_sum_pairs(arr) == {}

    def test_too_short_array(self):
        """Arrays shorter than 4 elements can never yield two distinct pairs."""
        assert find_equal_sum_pairs([]) == {}
        assert find_equal_sum_pairs([1]) == {}
        assert find_equal_sum_pairs([1, 2]) == {}
        assert find_equal_sum_pairs([1, 2, 3]) == {}

    def test_all_same_elements(self):
        """All identical elements — every pair has the same sum."""
        arr = [5, 5, 5, 5]
        results = find_equal_sum_pairs(arr)
        assert 10 in results
        assert len(results[10]) >= 2

    def test_negative_numbers(self):
        """Algorithm must handle negative integers correctly."""
        arr = [-1, -2, 3, 0, 1, 2]
        results = find_equal_sum_pairs(arr)
        for s, pairs in results.items():
            for a, b in pairs:
                assert a + b == s

    def test_large_numbers(self):
        """No integer overflow concerns in Python, but verify correctness."""
        arr = [10**9, 10**9 - 1, 1, 2, 10**9 + 1, -1]
        results = find_equal_sum_pairs(arr)
        for s, pairs in results.items():
            for a, b in pairs:
                assert a + b == s

    def test_duplicate_values_in_array(self):
        """Duplicates are treated as separate elements (index-based)."""
        arr = [1, 1, 2, 2]
        results = find_equal_sum_pairs(arr)
        # (1,2) appears multiple times → sum 3 should have multiple pairs
        assert 3 in results
        assert len(results[3]) >= 2

    def test_return_type(self):
        arr = [6, 4, 12, 10]
        results = find_equal_sum_pairs(arr)
        assert isinstance(results, dict)
        for key, val in results.items():
            assert isinstance(key, int)
            assert isinstance(val, list)
            for pair in val:
                assert isinstance(pair, tuple) and len(pair) == 2

    def test_each_pair_used_at_most_once(self):
        """The same (a,b) pair must not appear twice under the same sum."""
        arr = [6, 4, 12, 10, 22, 54, 32, 42, 21, 11]
        results = find_equal_sum_pairs(arr)
        for s, pairs in results.items():
            seen = set()
            for p in pairs:
                key = frozenset(p)
                assert key not in seen, f"Duplicate pair {p} under sum {s}"
                seen.add(key)
    
    def test_single_pair_sum_not_returned(self):
        arr = [1, 2, 3, 10]

        results = find_equal_sum_pairs(arr)

        for pairs in results.values():
            assert len(pairs) >= 2


# ---------------------------------------------------------------------------
# Formatting tests
# ---------------------------------------------------------------------------

class TestFormatResults:

    def test_output_contains_sum(self):
        arr = [4, 23, 65, 67, 24, 12, 86]
        results = find_equal_sum_pairs(arr)
        output = format_results(results)
        assert "have sum : 90" in output

    def test_output_line_structure(self):
        arr = [6, 4, 12, 10, 22, 54, 32, 42, 21, 11]
        results = find_equal_sum_pairs(arr)
        for line in format_results(results).splitlines():
            assert line.startswith("Pairs :"), f"Unexpected line: {line!r}"
            assert "have sum :" in line

    def test_empty_results_give_empty_string(self):
        assert format_results({}) == ""

    def test_format_results_deterministic(self):
        arr = [6, 4, 12, 10]
        r1 = format_results(find_equal_sum_pairs(arr))
        r2 = format_results(find_equal_sum_pairs(arr))
        assert r1 == r2

    def test_large_random_input(self):
        import random

        arr = [random.randint(-1000, 1000) for _ in range(200)]

        results = find_equal_sum_pairs(arr)

        for s, pairs in results.items():
            for a, b in pairs:
                assert a + b == s

    def test_results_order_independent(self):
        arr = [4, 23, 65, 67, 24, 12, 86]

        expected = {
            90: [(4, 86), (23, 67)]
        }

        assert result_as_set(find_equal_sum_pairs(arr)) == result_as_set(expected)



# ---------------------------------------------------------------------------
# find_equal_sum public alias
# ---------------------------------------------------------------------------

class TestFindEqualSum:

    def test_alias_returns_dict_by_default(self):
        result = find_equal_sum([6, 4, 12, 10, 22, 54, 32, 42, 21, 11])
        assert isinstance(result, dict)
        assert 16 in result

    def test_alias_formatted_returns_string(self):
        result = find_equal_sum([6, 4, 12, 10, 22, 54, 32, 42, 21, 11], formatted=True)
        assert isinstance(result, str)
        assert "have sum : 16" in result

    def test_alias_matches_underlying_function(self):
        arr = [4, 23, 65, 67, 24, 12, 86]
        assert find_equal_sum(arr) == find_equal_sum_pairs(arr)

    def test_alias_no_results_returns_empty_dict(self):
        assert find_equal_sum([1, 2, 4, 8]) == {}

    def test_alias_no_results_formatted_returns_empty_string(self):
        assert find_equal_sum([1, 2, 4, 8], formatted=True) == ""


# ---------------------------------------------------------------------------
# _parse_numbers — input style handling
# ---------------------------------------------------------------------------

class TestParseNumbers:

    def test_space_separated(self):
        assert _parse_numbers(["1", "2", "3", "4"]) == [1, 2, 3, 4]

    def test_comma_separated_single_token(self):
        # shell passes "1,2,3,4" as one token
        assert _parse_numbers(["1,2,3,4"]) == [1, 2, 3, 4]

    def test_comma_and_spaces_multiple_tokens(self):
        # shell passes "1," "2," "3," "4" as separate tokens
        assert _parse_numbers(["1,", "2,", "3,", "4"]) == [1, 2, 3, 4]

    def test_comma_with_spaces_in_one_string(self):
        # quoted on the CLI: "1, 2, 3, 4"
        assert _parse_numbers(["1, 2, 3, 4"]) == [1, 2, 3, 4]

    def test_mixed_spacing_around_commas(self):
        assert _parse_numbers(["1,", " 2,", " 4,", " 6,", " 3,", " 1"]) == [1, 2, 4, 6, 3, 1]

    def test_negative_numbers_space(self):
        assert _parse_numbers(["-1", "2", "-3"]) == [-1, 2, -3]

    def test_negative_numbers_comma(self):
        assert _parse_numbers(["-1,2,-3"]) == [-1, 2, -3]

    def test_invalid_token_exits(self):
        with pytest.raises(SystemExit):
            _parse_numbers(["1", "abc", "3"])

    def test_empty_string_token(self):
        with pytest.raises(SystemExit):
            _parse_numbers([""])

    def test_whitespace_token(self):
        with pytest.raises(SystemExit):
            _parse_numbers(["   "])

    def test_trailing_comma(self):
        with pytest.raises(SystemExit):
            _parse_numbers(["1,2,3,"])

    def test_double_comma(self):
        with pytest.raises(SystemExit):
            _parse_numbers(["1,,2"])

    @pytest.mark.parametrize("bad", [
        "1.5",
        "NaN",
        "inf",
        "0x10",
    ])
    def test_non_integer_values(self, bad):
        with pytest.raises(SystemExit):
            _parse_numbers([bad])


# ---------------------------------------------------------------------------
# CLI — input style integration tests
# ---------------------------------------------------------------------------

SCRIPT = "equal_sum_pairs.py"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )


class TestCLI:

    def test_plain_text_output(self):
        proc = _run("6", "4", "12", "10", "22", "54", "32", "42", "21", "11")
        assert proc.returncode == 0
        assert "have sum : 16" in proc.stdout

    def test_json_output_is_valid(self):
        proc = _run("6", "4", "12", "10", "22", "54", "32", "42", "21", "11", "--json")
        assert proc.returncode == 0
        data = json.loads(proc.stdout)
        assert "16" in data
        assert isinstance(data["16"], list)
        assert [6, 10] in data["16"] or [4, 12] in data["16"]

    def test_json_keys_are_sorted(self):
        proc = _run("6", "4", "12", "10", "22", "54", "32", "42", "21", "11", "--json")
        data = json.loads(proc.stdout)
        keys = [int(k) for k in data.keys()]
        assert keys == sorted(keys)

    def test_no_args_runs_examples(self):
        proc = _run()
        assert proc.returncode == 0
        assert "have sum" in proc.stdout

    def test_no_match_message(self):
        proc = _run("1", "2", "4", "8")
        assert "No pairs" in proc.stdout

    def test_no_match_json_message(self):
        proc = _run("1", "2", "4", "8", "--json")
        data = json.loads(proc.stdout)
        assert "message" in data

    def test_help_flag(self):
        proc = _run("--help")
        assert proc.returncode == 0
        assert "usage:" in proc.stdout.lower()

    def test_invalid_input_exits_nonzero(self):
        proc = _run("1", "abc", "3")
        assert proc.returncode != 0

    def test_comma_separated_no_spaces(self):
        proc = _run("1,2,4,6,3,1")
        assert proc.returncode == 0
        assert "have sum" in proc.stdout

    def test_comma_separated_with_spaces(self):
        # simulates: python script.py "1, 2, 4, 6, 3, 1"  (quoted on shell)
        proc = _run("1, 2, 4, 6, 3, 1")
        assert proc.returncode == 0
        assert "have sum" in proc.stdout

    def test_comma_and_space_tokens(self):
        # simulates: python script.py 1, 2, 4, 6, 3, 1  (unquoted — shell splits on spaces)
        proc = _run("1,", "2,", "4,", "6,", "3,", "1")
        assert proc.returncode == 0
        assert "have sum" in proc.stdout

    def test_space_and_comma_give_same_result(self):
        space = _run("6", "4", "12", "10", "22", "54", "32", "42", "21", "11")
        comma = _run("6,4,12,10,22,54,32,42,21,11")
        assert space.stdout == comma.stdout



class TestPrintResults:

    def test_print_does_not_raise(self, capsys):
        print_results([6, 4, 12, 10, 22, 54, 32, 42, 21, 11])
        captured = capsys.readouterr()
        assert "have sum" in captured.out

    def test_no_pairs_message(self, capsys):
        print_results([1, 2, 4, 8])
        captured = capsys.readouterr()
        assert "No pairs" in captured.out