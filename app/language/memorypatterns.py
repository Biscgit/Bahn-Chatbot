import builtins
from dataclasses import replace


# executes memory management
mem_patterns: list[tuple[str, builtins.callable]] = [
    (
        r"(at|from)\s?(\d)?(\d)?(am|pm)(.*)",
        lambda data, *args: replace(
            data,
            time=int(args[1] + args[2] if args[2] else args[1]) + 12 if args[3] == 'pm' else 0
        )
    ),
    (
        r"(.)*(with|using|line|route of)(\s\D*)(\d*)",
        lambda data, *args: replace(
            data,
            train=f"{args[2]}{args[3]}".replace(" ", "")
        )
    ),
    (
        r"(.*)\bfrom\b(?:\sstation)?\s([\w\s]*?)(?:\b\sto\b\s|$)(.*)",
        lambda data, *args: replace(
            data,
            station=args[1]
        )
    ),
    (
        r"(.*)\bto\b(?:\sstation)?\s([\w\s]*?)(?:\b\sfrom\b\s|$)(.*)",
        lambda data, *args: replace(
            data,
            end_station=args[1]
        )
    ),
    (
        r"(.*)\b(in)\b\s(\w*)",
        lambda data, *args: replace(
            data,
            station=args[2]
        )
    ),
    (
        r"does\s(([\w\s]*?)\s)have",
        lambda data, *args: replace(
            data,
            station=args[1]
        )
    )
]
