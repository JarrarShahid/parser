import re

class NumberExtractor:
    def __init__(self):
        # Canonical mapping for numbers 1–10
        self.word_to_num = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
        }

        # Expansions (capitalization variations)
        self.number_expansions = {
            "one": ["ONE", "One"],
            "two": ["TWO", "Two"],
            "three": ["THREE", "Three"],
            "four": ["FOUR", "Four"],
            "five": ["FIVE", "Five"],
            "six": ["SIX", "Six"],
            "seven": ["SEVEN", "Seven"],
            "eight": ["EIGHT", "Eight"],
            "nine": ["NINE", "Nine"],
            "ten": ["TEN", "Ten"],
        }

    def extract(self, sentence: str):
        """
        Extract numbers (digits or spelled out, 1–10) from a sentence.
        Returns a list of integers.
        """
        numbers_found = []

        # Normalize for matching
        text = sentence.lower()

        # --- 1. Find numeric digits (1–10) ---
        digit_matches = re.findall(r"\b([1-9]|10)\b", text)
        numbers_found.extend(int(num) for num in digit_matches)

        # --- 2. Find spelled-out numbers (with expansions) ---
        for word, value in self.word_to_num.items():
            # Match base word (lowercase)
            if re.search(rf"\b{word}\b", text):
                numbers_found.append(value)

            # Match expansions (case variations)
            for expansion in self.number_expansions.get(word, []):
                if re.search(rf"\b{expansion}\b", sentence):
                    numbers_found.append(value)

        return numbers_found

# extractor = NumberExtractor()

# print(extractor.extract("I have one hammer and 3 apples."))
# Output: [1, 3]

# print(extractor.extract("She bought TWO oranges and Ten bananas."))
# Output: [2, 10]

# print(extractor.extract("We saw eight birds."))
# Output: [8]
