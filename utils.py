from typing import List
import re


class NewsAnalyzer:
    def __init__(
        self,
        title_locator: str,
        description_locator: str,
        time_locator: str,
        phrase: str,
    ):
        self.title_locator = title_locator
        self.description_locator = description_locator
        self.time_locator = time_locator
        self.phrase = phrase

    def count_phrase(self, text: str, phrase: str) -> int:
        text = text.lower()
        phrase = phrase.lower()
        pattern = re.escape(phrase)
        matches = re.findall(pattern, text)
        return len(matches)

    def contains_money(self, text: str) -> bool:
        patterns = [
            r"\$\d{1,3}(,\d{3})*(\.\d{2})?",  # Format like $11.1 or $111,111.11
            r"\b\d+(?:\.\d{2})? dollars\b",  # Format like 11 dollars or 11.11 dollars
            r"\b\d+(?:\.\d{2})? USD\b",  # Format like 11 USD or 11.11 USD
        ]
        combined_pattern = "|".join(patterns)
        if re.search(combined_pattern, text, re.IGNORECASE):
            return True
        return False

    def process_row(self) -> List[List]:

        title = self.title_locator
        description = self.description_locator
        ts = self.time_locator
        money = self.contains_money(description)
        phrase_count = self.count_phrase(description, self.phrase)
        phrase_count += self.count_phrase(title, self.phrase)

        row = [title, description, ts, money, phrase_count]
        return row
