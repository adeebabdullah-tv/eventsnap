from datetime import date

from normalizer import normalize_date, normalize_time


reference_date = date(2026, 9, 15)


tests = [
    ("2026-09-20", "2026-09-20"),
    ("September 20", "2026-09-20"),
    ("tomorrow", "2026-09-16"),
    ("today", "2026-09-15"),
    ("day after tomorrow", "2026-09-17"),
]


print("DATE TESTS")
print("-" * 30)

for input_date, expected in tests:
    result = normalize_date(input_date, reference_date)

    print(
        f"{input_date:20} → {result} "
        f"{'✅' if str(result) == expected else '❌'}"
    )


time_tests = [
    ("10 AM", "10:00:00"),
    ("2 PM", "14:00:00"),
    ("10:30 AM", "10:30:00"),
    ("2:45 PM", "14:45:00"),
]


print("\nTIME TESTS")
print("-" * 30)

for input_time, expected in time_tests:
    result = normalize_time(input_time)

    print(
        f"{input_time:20} → {result} "
        f"{'✅' if str(result) == expected else '❌'}"
    )