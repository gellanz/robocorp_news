from utils import NewsAnalyzer
import pandas as pd
from typing import List
import time


class Robot:
    def __init__(self, browser, phrase, type_news, sort_by):
        self.browser = browser
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.browser.configure(headless=True)
        self.browser.configure_context(user_agent=user_agent)
        self.phrase = phrase
        self.type_news = type_news
        self.sort_by = sort_by

    def navigate(self):
        # Launch the browser with custom user agent
        self.browser.goto("https://www.latimes.com/")
        # Navigate to the initial webpage
        page = self.browser.page()
        time.sleep(2)
        page.wait_for_load_state()

        # Interact with the search bar
        page.click(
            "body > ps-header > header > div.flex.\[\@media_print\]\:hidden > button"
        )

        time.sleep(1)

        page.fill(
            "body > ps-header > header > div.flex.\[\@media_print\]\:hidden > div.ct-hidden.fixed.md\:absolute.top-12\.5.right-0.bottom-0.left-0.z-25.bg-header-bg-color.md\:top-15.md\:bottom-auto.md\:h-25.md\:shadow-sm-2 > form > label > input",
            self.phrase,
        )  # Adjust selector and query as needed

        time.sleep(1)

        page.click(
            "body > ps-header > header > div.flex.\[\@media_print\]\:hidden > div.ct-hidden.fixed.md\:absolute.top-12\.5.right-0.bottom-0.left-0.z-25.bg-header-bg-color.md\:top-15.md\:bottom-auto.md\:h-25.md\:shadow-sm-2 > form > button"
        )
        time.sleep(1)
        # Wait for navigation to the results page

        # politics
        page.click(
            f"body > div.page-content > ps-search-results-module > form > div.search-results-module-ajax > ps-search-filters > div > aside > div > div.search-results-module-filters-content.SearchResultsModule-filters-content > div:nth-child(1) > ps-toggler > ps-toggler > div > ul > li:nth-child({self.type_news}) > div > div.checkbox-input > label > input"
        )

        time.sleep(1)

        date_locator = page.locator(
            "body > div.page-content > ps-search-results-module > form > div.search-results-module-ajax > ps-search-filters > div > main > div.search-results-module-results-header > div.search-results-module-sorts > div > label > select"
        )
        date_locator.select_option(self.sort_by)
        page.wait_for_load_state()

        time.sleep(1)

        news_locator = page.locator("ul > li")
        return news_locator

    def process_ul_element(self, news_locator):
        title_locator = news_locator.locator(".promo-title")
        description_locator = news_locator.locator(".promo-description")
        time_locator = news_locator.locator(".promo-timestamp")
        dataset = []
        for i in range(9):
            news_analizer = NewsAnalyzer(
                title_locator=title_locator.nth(i).all_inner_texts()[0],
                description_locator=description_locator.nth(i).all_inner_texts()[0],
                time_locator=time_locator.nth(i).all_inner_texts()[0],
                phrase=self.phrase,
            )

            row = news_analizer.process_row()
            dataset.append(row)
        return dataset

    def export_to_excel(self, dataset: List[List], output_path) -> None:
        columns = [
            "Title",
            "Description",
            "Timestamp",
            "Title Contains Money",
            "Phrase Count",
        ]
        df = pd.DataFrame(dataset, columns=columns)
        df.to_excel(output_path, index=False)
        print(f"DataFrame exported to {output_path}")
