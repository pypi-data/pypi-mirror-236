"""
    Bucket for categorizing emoji skin tone
    usage
"""

# built-in
from typing import Any, Dict, List, Type, cast

# internal
from instagram_bucketizer.buckets import (
    EN_EMOJI_TO_UNICODE,
    Bucket,
    Comment,
    DataColumns,
    TBucket,
    base_columns,
)

skin_tone_str = [
    "dark_skin_tone",
    "light_skin_tone",
    "medium_skin_tone",
    "medium-dark_skin_tone",
    "medium-light_skin_tone",
]


def get_tone_str(emoji: str):
    """
    Parse and return the skin tone
    substr if available
    """
    for tone in skin_tone_str:
        if "_" + tone in emoji:
            return tone
    return ""


def is_modifiable(emoji: str) -> bool:
    """
    Detect if the given emoji str
    is modifiable by skin tone
    """
    cleaned = emoji.replace(":", "")
    for tone in skin_tone_str:
        if tone in cleaned:
            return True

        if f":{cleaned}_{tone}:" in EN_EMOJI_TO_UNICODE:
            return True
    return False


def get_base_emoji(emoji: str) -> str:
    """
    Strip a tone substr if available
    """
    tone_str = get_tone_str(emoji)
    return emoji.replace(tone_str, "")


columns: Dict[str, List[Any]] = {
    "Emoji Total": [],
    "Emoji Modifiable": [],
    "Emoji Skin Neutral": [],
    "Emoji Skin Light": [],
    "Emoji Skin Medium Light": [],
    "Emoji Skin Medium": [],
    "Emoji Skin Medium Dark": [],
    "Emoji Skin Dark": [],
}


class SkinToneBucket(Bucket):
    """
    Bucket to add up all modifiable skin tone emojis
    """

    def __init__(self, comment: Comment):
        super().__init__(comment)
        self.comment_text = comment["text"]
        self.emojis = Bucket.process_emojis(cast(str, self.comment_text))

        self.total_emoji = len(self.emojis)
        self.tone_emoji_counts = {tone: 0 for tone in skin_tone_str}

        self.tone_emoji_counts["modifiable"] = 0
        self.tone_emoji_counts["neutral"] = 0
        for emoji in self.emojis:
            if is_modifiable(emoji):
                self.tone_emoji_counts["modifiable"] += 1
                if get_base_emoji(emoji) == emoji:
                    self.tone_emoji_counts["neutral"] += 1
                    continue

            tone_str = get_tone_str(emoji)
            if tone_str:
                self.tone_emoji_counts[tone_str] += 1

    @staticmethod
    def get_columns() -> DataColumns:
        """
        Get the data columns for this bucket
        """
        cols = columns
        cols.update(base_columns)
        return cols

    @classmethod
    def from_comment(cls: Type[TBucket], comment: Comment) -> TBucket:
        """
        Create child class based on given comment data
        """
        return cls(comment)

    def to_excel_impl(self, data: DataColumns) -> None:
        """
        Given the premade data, adhereing to get_bucket_cols for each bucket
        append this child classes data and return
        """

        data["Emoji Total"].append(self.total_emoji)
        data["Emoji Modifiable"].append(self.tone_emoji_counts["modifiable"])
        data["Emoji Skin Neutral"].append(self.tone_emoji_counts["neutral"])
        data["Emoji Skin Light"].append(
            self.tone_emoji_counts["light_skin_tone"]
        )
        data["Emoji Skin Medium Light"].append(
            self.tone_emoji_counts["medium-light_skin_tone"]
        )
        data["Emoji Skin Medium"].append(
            self.tone_emoji_counts["medium_skin_tone"]
        )
        data["Emoji Skin Medium Dark"].append(
            self.tone_emoji_counts["medium-dark_skin_tone"]
        )
        data["Emoji Skin Dark"].append(
            self.tone_emoji_counts["dark_skin_tone"]
        )
