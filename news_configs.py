from typing import List

from robocorp import workitems
from robocorp.tasks import task
from dataclasses import dataclass
from typing import Literal


@dataclass
class NewsConfig:
    phrase: str
    sort_by: Literal["relevance", "newest", "oldest"]
    type_news: Literal["politics", "entertainment and arts", "science and medicine"]

    def sort_by_element(self):
        sort_by_dict = {"relevance": "0", "newest": "1", "oldest": "2"}
        return sort_by_dict[self.sort_by]

    def news_type(self):
        # la news turns out the checkboxes change depending on the search, TODO: fix
        news_dict = {
            "politics": "1",
            "entertainment and arts": "8",
            "science and medicine": "10",
        }
        return news_dict[self.type_news]

    def final_dict(self):
        return {
            "phrase": self.phrase,
            "sort_by": self.sort_by_element(),
            "type_news": self.news_type(),
        }


@task
def split_orders_file():
    """
    Read orders file from input item and split into outputs
    """

    search_news = [
        NewsConfig(phrase="covid", sort_by="newest", type_news="science and medicine"),
        NewsConfig(phrase="biden", sort_by="newest", type_news="politics"),
    ]

    for news_config in search_news:
        workitems.outputs.create(payload=news_config.final_dict())
