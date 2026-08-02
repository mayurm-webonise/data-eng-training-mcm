

from __future__ import annotations

import re

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------
# 1. How to import pandas and check the version?
# --------------------------------------------------------------------------
def get_pandas_version() -> str:
    """Return the installed pandas version string."""
    return pd.__version__


# --------------------------------------------------------------------------
# 2. How to create a series from a list, a numpy array, and a dict?
# --------------------------------------------------------------------------
def build_series_from_sources() -> tuple[pd.Series, pd.Series, pd.Series]:
    """Build three pandas Series from a list, a numpy array, and a dict."""
    letters = list("abcedfghijklmnopqrstuvwxyz")
    numbers = np.arange(26)
    letter_to_number = dict(zip(letters, numbers))

    series_from_list = pd.Series(letters)
    series_from_array = pd.Series(numbers)
    series_from_dict = pd.Series(letter_to_number)
    return series_from_list, series_from_array, series_from_dict


# --------------------------------------------------------------------------
# 6. How to get the items of series A not present in series B?
# --------------------------------------------------------------------------
def items_only_in_first(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
    """Return the items of series_a that do not appear in series_b."""
    return series_a[~series_a.isin(series_b)]


# --------------------------------------------------------------------------
# 10. Keep only the top-N most frequent values; replace everything else.
# --------------------------------------------------------------------------
def keep_top_n_frequent(
    series: pd.Series, top_n: int = 2, other_label: str = "Other"
) -> pd.Series:
    """Keep the top_n most frequent values as-is; replace the rest with other_label."""
    most_frequent_values = series.value_counts().index[:top_n]
    return series.where(series.isin(most_frequent_values), other_label)


# --------------------------------------------------------------------------
# 12. How to convert a numpy array (via a Series) to a dataframe of a given shape?
# --------------------------------------------------------------------------
def series_to_dataframe(series: pd.Series, n_rows: int, n_cols: int) -> pd.DataFrame:
    """Reshape a 1-D series' values into a dataframe with n_rows x n_cols."""
    return pd.DataFrame(series.to_numpy().reshape(n_rows, n_cols))


# --------------------------------------------------------------------------
# 22. Get day of month, week number, day of year, and day of week from date strings.
# --------------------------------------------------------------------------
def extract_date_parts(date_strings: pd.Series) -> pd.DataFrame:
    """Return day-of-month, ISO week number, day-of-year, and weekday name."""
    parsed_dates = pd.to_datetime(date_strings, format="mixed")
    return pd.DataFrame(
        {
            "day_of_month": parsed_dates.dt.day,
            "week_number": parsed_dates.dt.isocalendar().week.astype(int),
            "day_of_year": parsed_dates.dt.dayofyear,
            "day_of_week": parsed_dates.dt.day_name(),
        }
    )


# --------------------------------------------------------------------------
# 25. Filter valid emails out of a series of candidate strings.
# --------------------------------------------------------------------------
_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}")


def filter_valid_emails(candidates: pd.Series) -> pd.Series:
    """Return only the entries of `candidates` that look like valid emails."""
    is_email = candidates.str.match(_EMAIL_PATTERN)
    return candidates[is_email]


# --------------------------------------------------------------------------
# 51. Row position of the n-th largest value in a given column.
# --------------------------------------------------------------------------
def nth_largest_row_position(df: pd.DataFrame, column: str, n: int) -> int:
    """
    Return the 0-based row position of the n-th largest value (n=1 is the
    largest) in `column`.

    Note: the original tutorial solution used `argsort()[::-1][n]`, which a
    number of readers pointed out gives the wrong row (reversing an argsort
    result does not correctly invert it). Sorting descending directly and
    indexing avoids that bug.
    """
    return df[column].sort_values(ascending=False).index[n - 1]


# --------------------------------------------------------------------------
# 74. Frequency of unique values across an entire dataframe.
# --------------------------------------------------------------------------
def value_frequencies_whole_df(df: pd.DataFrame) -> pd.Series:
    """Return value counts computed over every cell in the dataframe."""
    return pd.Series(df.to_numpy().ravel()).value_counts()


# --------------------------------------------------------------------------
# 75. Split a single text column into multiple columns.
# --------------------------------------------------------------------------
def split_text_column(
    df: pd.DataFrame, column: str, delimiter_pattern: str = r",|\t"
) -> pd.DataFrame:
    """Split `column` on `delimiter_pattern`, using its first row as headers."""
    split_values = df[column].str.split(delimiter_pattern, expand=True)
    split_values.columns = split_values.iloc[0].str.strip()
    return split_values.iloc[1:].reset_index(drop=True)


def main() -> None:
    print("Q1: pandas version ->", get_pandas_version())

    print("\nQ2: series from list / array / dict")
    from_list, from_array, from_dict = build_series_from_sources()
    print(from_list.head(3).to_dict(), from_array.head(3).to_dict(), from_dict.head(3).to_dict())

    print("\nQ6: items in A not in B")
    ser1 = pd.Series([1, 2, 3, 4, 5])
    ser2 = pd.Series([4, 5, 6, 7, 8])
    print(items_only_in_first(ser1, ser2).tolist())

    print("\nQ10: keep top-2 frequent values")
    np.random.seed(100)
    freq_series = pd.Series(np.random.randint(1, 5, 12))
    print(keep_top_n_frequent(freq_series).tolist())

    print("\nQ12: series -> 7x5 dataframe")
    reshape_series = pd.Series(np.random.randint(1, 10, 35))
    print(series_to_dataframe(reshape_series, 7, 5))

    print("\nQ22: date part extraction")
    dates = pd.Series(
        ["01 Jan 2010", "02-02-2011", "20120303", "2013/04/04", "2014-05-05", "2015-06-06T12:20"]
    )
    print(extract_date_parts(dates))

    print("\nQ25: filter valid emails")
    emails = pd.Series(
        ["buying books at amazon.com", "rameses@egypt.com", "matt@t.co", "narendra@modi.com"]
    )
    print(filter_valid_emails(emails).tolist())

    print("\nQ51: row position of 5th largest value in column 'a'")
    np.random.seed(1)
    df51 = pd.DataFrame(np.random.randint(1, 30, 30).reshape(10, -1), columns=list("abc"))
    print(df51)
    print("Row position:", nth_largest_row_position(df51, "a", 5))

    print("\nQ74: value frequencies across whole dataframe")
    np.random.seed(1)
    df74 = pd.DataFrame(np.random.randint(1, 10, 20).reshape(-1, 4), columns=list("abcd"))
    print(value_frequencies_whole_df(df74))

    print("\nQ75: split text column")
    df75 = pd.DataFrame(
        [
            "STD, City\tState",
            "33, Kolkata\tWest Bengal",
            "44, Chennai\tTamil Nadu",
            "40, Hyderabad\tTelengana",
            "80, Bangalore\tKarnataka",
        ],
        columns=["row"],
    )
    print(split_text_column(df75, "row"))


if __name__ == "__main__":
    main()
