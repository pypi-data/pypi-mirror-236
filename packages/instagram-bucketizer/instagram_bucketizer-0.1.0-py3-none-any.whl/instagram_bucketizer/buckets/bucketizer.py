"""
Bucketizer class
"""

# built-in
import json
from typing import List

import pandas as pd

# third party
from vcorelib.paths import Pathlike, normalize

# internal
from instagram_bucketizer.buckets import Bucket, DataColumns

# This is used in detecting bucket subclasses
# pylint: disable=unused-import
# flake8: noqa
from instagram_bucketizer.buckets.emoji_tone import SkinToneBucket


def get_available_buckets() -> List[str]:
    """
    Return a list of available buckets
    """
    return [cls.__name__ for cls in Bucket.__subclasses__()]


def get_bucket(name: str) -> type[Bucket]:
    """
    Get a bucket class from string
    """
    for cls in Bucket.__subclasses__():
        if cls.__name__ == name:
            return cls
    assert False, (
        f"Bucket {name} is not" + f" available ({get_available_buckets()})"
    )


class Bucketizer:
    """
    Given a string, get corresponding bucket child name
    hand list of comment dicts, create buckets
    print to excel
    """

    def __init__(self, bucket: str) -> None:
        available = get_available_buckets()
        assert (
            bucket in available
        ), f"Bucket {bucket} not in availble bucket!\n available: {available}!"

        self.bucket: type[Bucket] = get_bucket(bucket)
        self.comments: List[Bucket] = []
        self.post_code = ""

    def load_comments(self, comments_file: Pathlike) -> None:
        """
        Load all the comments in a file
        """
        comments_file = normalize(comments_file)
        with open(comments_file, "r", encoding="utf-8") as read_fd:
            data = json.load(read_fd)
            self.post_code = data["post_code"]
            for comment in data["comments"]:
                self.comments.append(self.bucket.from_comment(comment))

    def extend(self, data: DataColumns) -> None:
        """
        Given data struct, extend it with own data
        """
        for comment in self.comments:
            comment.to_excel(data, self.post_code)

    def get_data(self) -> DataColumns:
        """
        Return a header row plus bucket data
        """
        data = self.bucket.get_columns()
        self.extend(data)
        return data

    def write(self, data: DataColumns, output_file: Pathlike) -> None:
        """
        Write given data to the output file
        """
        output_file = normalize(output_file)
        output_data = pd.DataFrame(data=data)
        output_data.to_excel(output_file)
