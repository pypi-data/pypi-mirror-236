"""
Base bucket abstract class
"""

# built-in
from abc import ABC, abstractmethod
from typing import Dict, List, Type, TypeVar, Union, cast

# third-party
import emoji as _emoji
from emoji import EMOJI_DATA, EmojiMatch

# generic type names dont need to be snake
# pylint: disable=invalid-name
TBucket = TypeVar("TBucket", bound="Bucket")
Comment = Dict[str, Union[int, str]]
Comments = List[Comment]
DataColumns = Dict[str, List[Union[int, str]]]

base_columns: DataColumns = {
    "post_id": [],
    "comment": [],
    "username": [],
    "datetime": [],
    "likes": [],
    "replies": [],
}

# Simplify the large structure to just english
EN_EMOJI_TO_UNICODE = {}
for uni, edat in EMOJI_DATA.items():
    EN_EMOJI_TO_UNICODE[edat["en"]] = uni


class Bucket(ABC):
    """
    Abstract class that should be able to be created from a comment
    process, then be called on to write to a dictionary
    of arrays to be exported to panda frame
    """

    def __init__(self, comment: Comment) -> None:
        self.comment = comment

    @staticmethod
    def get_columns() -> DataColumns:
        """
        Return this bucket's columns
        """
        return base_columns

    @staticmethod
    def process_emojis(comment_txt: str) -> List[str]:
        """
        Get a list of available emojis in a comment
        """
        tot_emoj = list(
            _emoji.analyze(
                _emoji.emojize(comment_txt), non_emoji=False, join_emoji=True
            )
        )
        emojis: List[str] = []
        if tot_emoj:
            for em in tot_emoj:
                assert isinstance(em.value, EmojiMatch)
                assert em.value.data
                emojis.append(em.value.data["en"])
        return emojis

    @classmethod
    def from_comment(cls: Type[TBucket], comment: Comment) -> TBucket:
        """
        Create child class based on given comment data
        """
        return cls(comment)

    def to_excel(self, data: DataColumns, post_id: str) -> None:
        """
        Add general comment data, then call child impl
        """

        data["post_id"].append(post_id)
        data["comment"].append(self.comment["text"])
        data["username"].append(self.comment["username"])
        data["datetime"].append(self.comment["created_at"])
        data["likes"].append(self.comment["likes_count"])
        data["replies"].append(
            len(cast(List[Comment], self.comment["answers"]))
        )
        self.to_excel_impl(data)

    @abstractmethod
    def to_excel_impl(self, data: DataColumns) -> None:
        """
        Given the premade data, adhereing to get bucket_cols for each bucket
        append this child classes data and return
        """
