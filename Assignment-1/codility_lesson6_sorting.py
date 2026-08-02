

from __future__ import annotations


# --------------------------------------------------------------------------
# Distinct: count the number of distinct values in an array.
# --------------------------------------------------------------------------
def solution_distinct(a: list[int]) -> int:
    """Return the number of distinct values in a."""
    return len(set(a))


# --------------------------------------------------------------------------
# MaxProductOfThree: maximize A[P] * A[Q] * A[R] for any triplet P < Q < R.
# --------------------------------------------------------------------------
def solution_max_product_of_three(a: list[int]) -> int:
    """
    Return the maximal product of any 3 elements of a.

    The best triplet is either the three largest values, or the two most
    negative values (whose product is positive) combined with the single
    largest value -- so only the sorted extremes need to be compared.
    """
    sorted_a = sorted(a)
    product_of_three_largest = sorted_a[-1] * sorted_a[-2] * sorted_a[-3]
    product_of_two_smallest_and_largest = sorted_a[0] * sorted_a[1] * sorted_a[-1]
    return max(product_of_three_largest, product_of_two_smallest_and_largest)


# --------------------------------------------------------------------------
# Triangle: does a triangular triplet (P, Q, R) exist, where the sum of any
# two sides exceeds the third?
# --------------------------------------------------------------------------
def solution_triangle(a: list[int]) -> int:
    """
    Return 1 if a triangular triplet exists in a, otherwise 0.

    After sorting, if any triangular triplet exists at all, three
    *consecutive* elements will form one -- so only adjacent triples need
    checking, giving an O(N log N) algorithm overall.
    """
    sorted_a = sorted(a)
    for i in range(len(sorted_a) - 2):
        smallest, middle, largest = sorted_a[i], sorted_a[i + 1], sorted_a[i + 2]
        if smallest + middle > largest:
            return 1
    return 0


def main() -> None:
    print(
        "Distinct([2, 1, 1, 2, 3, 1]) ->",
        solution_distinct([2, 1, 1, 2, 3, 1]),  # expect 3
    )

    print(
        "MaxProductOfThree([-3, 1, 2, -2, 5, 6]) ->",
        solution_max_product_of_three([-3, 1, 2, -2, 5, 6]),  # expect 60
    )

    print(
        "Triangle([10, 2, 5, 1, 8, 20]) ->",
        solution_triangle([10, 2, 5, 1, 8, 20]),  # expect 1
    )
    print(
        "Triangle([10, 50, 5, 1]) ->",
        solution_triangle([10, 50, 5, 1]),  # expect 0
    )


if __name__ == "__main__":
    main()
