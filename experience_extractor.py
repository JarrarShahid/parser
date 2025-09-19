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

        self.filter_approximation = {
            "around": {
                "keywords": ["around", "approximately", "about", "close to"],
                "operator": "=",
            },
            "more": {
                "keywords": ["more than", "greater than", "over", "at least"],
                "operator": "=>",
            },
            "less": {
                "keywords": ["less than", "under", "below", "at most"],
                "operator": "=<",
            },
        }

    def extract(self, sentence: str):
        """
        Extract numbers (digits or spelled out, 1–10) and map context
        to approximation filters (=, =>, =<).
        Returns list of tuples: (number, operator).
        """
        numbers = set()  # use a set to avoid duplicates

        # Normalize
        text = sentence.lower()

        # --- 1. Find numeric digits (1–10) ---
        digit_matches = re.findall(r"\b([1-9]|10)\b", text)
        numbers.update(int(num) for num in digit_matches)

        # --- 2. Find spelled-out numbers ---
        for word, value in self.word_to_num.items():
            if re.search(rf"\b{word}\b", text):
                numbers.add(value)
            for expansion in self.number_expansions.get(word, []):
                if re.search(rf"\b{expansion}\b", sentence):
                    numbers.add(value)

        # --- 3. Detect context (around/more/less) ---
        operator = "="  # default
        for key, mapping in self.filter_approximation.items():
            for kw in mapping["keywords"]:
                if kw in text:
                    operator = mapping["operator"]
                    break

        # Return list of (number, operator) tuples
        return [(num, operator) for num in numbers]

# extractor = NumberExtractor()

# print(extractor.extract("I have around five years of experience"))
# [(5, '=')]

# print(extractor.extract("I have more than three years of experience"))
# [(5, '=>')]

# print(extractor.extract("My experience is less than TWO years"))
# [(5, '=<')]

