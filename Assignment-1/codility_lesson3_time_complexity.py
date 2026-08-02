

from __future__ import annotations


# --------------------------------------------------------------------------
# FrogJmp: minimal number of fixed-size jumps of length d to get from x to
# a position >= y.
# --------------------------------------------------------------------------
def solution_frog_jmp(x: int, y: int, d: int) -> int:
    """Return the minimal number of jumps of size d to reach >= y from x."""
    distance_to_cover = y - x
    # Ceiling division without floating point, safe for very large inputs.
    return -(-distance_to_cover // d)


# --------------------------------------------------------------------------
# PermMissingElem: an array holds every integer in [1..N+1] except one;
# find the missing value.
# --------------------------------------------------------------------------
def solution_perm_missing_elem(a: list[int]) -> int:
    """Return the single integer missing from a permutation of 1..(len(a)+1)."""
    n = len(a)
    expected_sum = (n + 1) * (n + 2) // 2
    return expected_sum - sum(a)


# --------------------------------------------------------------------------
# TapeEquilibrium: split the array into two non-empty parts and minimize
# the absolute difference between their sums.
# --------------------------------------------------------------------------
def solution_tape_equilibrium(a: list[int]) -> int:
    """Return the minimal |left_sum - right_sum| over every valid split of a."""
    total = sum(a)
    left_sum = 0
    min_difference: int | None = None

    for value in a[:-1]:  # the split point can't be after the last element
        left_sum += value
        right_sum = total - left_sum
        difference = abs(left_sum - right_sum)
        if min_difference is None or difference < min_difference:
            min_difference = difference

    return min_difference


def main() -> None:
    print("FrogJmp(10, 85, 30) ->", solution_frog_jmp(10, 85, 30))  # expect 3

    print(
        "PermMissingElem([2, 3, 1, 5]) ->",
        solution_perm_missing_elem([2, 3, 1, 5]),  # expect 4
    )

    print(
        "TapeEquilibrium([3, 1, 2, 4, 3]) ->",
        solution_tape_equilibrium([3, 1, 2, 4, 3]),  # expect 1
    )


if __name__ == "__main__":
    main()
