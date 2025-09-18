import re

def extract_numbers(sentence: str):
    # Mapping of spelled-out numbers to digits
    word_to_num = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10
    }

    # Normalize text (lowercase for word matching)
    text = sentence.lower()

    numbers_found = []

    # --- 1. Find numeric digits (1–10) ---
    digit_matches = re.findall(r"\b([1-9]|10)\b", text)
    numbers_found.extend(int(num) for num in digit_matches)

    # --- 2. Find spelled-out numbers ---
    for word, value in word_to_num.items():
        if re.search(rf"\b{word}\b", text):
            numbers_found.append(value)

    return numbers_found


# ---------- Example Usage ----------
examples = [
    "I have one hammer",
    "I have five apples",
    "She bought Seven oranges",
    "We need ten chairs",
    "Bring 2 and nine more"
]

for ex in examples:
    print(f"{ex}  ->  {extract_numbers(ex)}")
