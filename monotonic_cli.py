import argparse
import sys
import time
from typing import Callable, List, Optional, Tuple

MAX_RECURSIVE_LEN = 950
RECURSION_LIMIT_BUFFER = 200
RECURSION_LIMIT_CAP = 3000


def _normalize_and_validate_digits(s: str) -> str:
    if s is None:
        raise ValueError("Input kosong.")
    s = s.strip()
    if not s:
        raise ValueError("Input kosong.")
    if not s.isdigit():
        raise ValueError("Input harus berupa digit saja (0-9).")
    return s


def check_monotonic_iterative(s: str) -> str:
    """
    Kembalikan salah satu:
    - "naik"  (non-decreasing)
    - "turun" (non-increasing)
    - "tidak monotonik"

    Catatan: angka dengan semua digit sama (mis. "1111") dianggap "naik"
    (non-decreasing) sesuai konvensi.
    """
    s = _normalize_and_validate_digits(s)
    if len(s) <= 1:
        return "naik"

    has_increase = False
    has_decrease = False

    for i in range(1, len(s)):
        if s[i] > s[i - 1]:
            has_increase = True
        elif s[i] < s[i - 1]:
            has_decrease = True

        if has_increase and has_decrease:
            return "tidak monotonik"

    if has_decrease:
        return "turun"
    return "naik"


def check_monotonic_recursive(s: str) -> str:
    s = _normalize_and_validate_digits(s)
    if len(s) <= 1:
        return "naik"
    if len(s) > MAX_RECURSIVE_LEN:
        raise ValueError(
            f"Input terlalu panjang untuk rekursif (maks {MAX_RECURSIVE_LEN} digit)."
        )

    desired_limit = len(s) + RECURSION_LIMIT_BUFFER
    current_limit = sys.getrecursionlimit()
    if desired_limit > current_limit:
        sys.setrecursionlimit(min(desired_limit, RECURSION_LIMIT_CAP))

    # trend: 0 = unknown/flat, 1 = nondecreasing, -1 = nonincreasing, 2 = not monotonic
    def _helper(pos: int, trend: int) -> int:
        if pos >= len(s):
            return trend

        prev_digit = s[pos - 1]
        curr_digit = s[pos]

        if curr_digit > prev_digit:
            if trend == -1:
                return 2
            trend = 1
        elif curr_digit < prev_digit:
            if trend == 1:
                return 2
            trend = -1

        return _helper(pos + 1, trend)

    trend = _helper(1, 0)
    if trend == 2:
        return "tidak monotonik"
    if trend == -1:
        return "turun"
    return "naik"


def measure_time(func: Callable[[str], str], s: str, trials: int = 5) -> Tuple[str, float]:
    if trials < 1:
        raise ValueError("trials harus >= 1.")

    times_ms: List[float] = []
    result: Optional[str] = None

    for _ in range(trials):
        start = time.perf_counter()
        result = func(s)
        end = time.perf_counter()
        times_ms.append((end - start) * 1000)

    assert result is not None
    return result, sum(times_ms) / len(times_ms)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bandingkan algoritma iteratif vs rekursif untuk mengecek bilangan monotonik (digit)."
    )
    parser.add_argument(
        "digits",
        nargs="?",
        help='Bilangan dalam bentuk string digit, contoh: "12345"',
    )
    parser.add_argument("--trials", type=int, default=5, help="Jumlah pengulangan timing.")
    args = parser.parse_args()

    raw_digits = args.digits or input("Masukkan bilangan (digit saja): ")
    try:
        digits = _normalize_and_validate_digits(raw_digits)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    print(f"\nInput: {digits} (panjang = {len(digits)})\n")

    result_it, time_it = measure_time(check_monotonic_iterative, digits, trials=args.trials)
    print(f"Iteratif : {result_it}")
    print(f"Waktu    : {time_it:.6f} ms\n")

    try:
        result_rec, time_rec = measure_time(
            check_monotonic_recursive, digits, trials=args.trials
        )
        print(f"Rekursif : {result_rec}")
        print(f"Waktu    : {time_rec:.6f} ms\n")
    except (ValueError, RecursionError) as exc:
        print(f"Rekursif : gagal ({exc})\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
