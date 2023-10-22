"""
    Pull comments from a post(s) and place into a comments file.
"""

# built-in
import argparse
from datetime import datetime
import json
from pathlib import Path
import time
from typing import Union

# third-party
import emoji
from instaloader import Instaloader, Post  # type: ignore [attr-defined]
from tqdm import tqdm
from vcorelib.args import CommandFunction
from vcorelib.paths import normalize

# internal
from instagram_bucketizer.buckets import Comments


def normalize_to_datestr(date: Union[str, int, datetime]) -> str:
    """
    Given a epoch, str, or datetime, make sure its a str
    """

    if isinstance(date, str):
        return date
    if isinstance(date, int):
        return str(datetime.fromtimestamp(date))
    if isinstance(date, datetime):
        return str(date)
    assert False, f"Given data {date} is invalid! {type(date)}"


def normalize_to_epoch(date: Union[str, float, int, datetime]) -> float:
    """
    Given a epoch, str, or datetime obj make sure its an int
    """

    if isinstance(date, str):
        utc_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return ((utc_time) - datetime(1970, 1, 1)).total_seconds()
    if isinstance(date, int):
        return float(date)
    if isinstance(date, datetime):
        return date.timestamp()
    if isinstance(date, float):
        return date
    assert False, f"Given data {date} is invalid! {type(date)}"


def to_emoji_str(emoji_str: str) -> str:
    """
    Translate utf-16 to emoji strings
    """
    return emoji_str.encode("utf-16-be", "surrogatepass").decode("utf-16-be")


def write_post(
    args: argparse.Namespace, post_code: str, comments: Comments
) -> None:
    """
    Write data out
    """
    output_dir = normalize(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    sorted_data = sorted(
        comments, key=lambda x: normalize_to_epoch(x["created_at"])
    )
    for data in sorted_data:
        data["text"] = emoji.demojize(to_emoji_str(str(data["text"])))

    full_out = {"post_code": post_code, "comments": sorted_data}
    with open(
        output_dir.joinpath(f"{args.prefix}_{post_code}.json"),
        "w",
        encoding="UTF-8",
    ) as com_file:
        com_file.write(json.dumps(full_out, indent=4))


def parse_post_cmd(args: argparse.Namespace):
    """
    for each post code, get data, load into dictionary and return
    """
    assert args.username, "No username provided!"
    loader = Instaloader()
    loader.load_session_from_file(args.username)

    for post_code in args.post_codes:
        post = Post.from_shortcode(loader.context, post_code)
        print(f"Loading comments from {post_code}")
        with loader.context.error_catcher("Comment Parsing:"):
            ret_data: Comments = []
            with tqdm(total=post.comments) as progress_counter:
                for comment in post.get_comments():
                    ret_data.append(
                        {
                            "id": comment.id,
                            "created_at": normalize_to_datestr(
                                comment.created_at_utc
                            ),
                            "text": comment.text,
                            "username": comment.owner.username,
                            "likes_count": comment.likes_count,
                            "answers": sorted(  # type: ignore[dict-item]
                                [
                                    {
                                        "id": answer.id,
                                        "created_at": normalize_to_datestr(
                                            answer.created_at_utc
                                        ),
                                        "text": answer.text,
                                        "username": answer.owner.username,
                                        "likes_count": answer.likes_count,
                                    }
                                    for answer in comment.answers
                                ],
                                key=lambda x: normalize_to_epoch(
                                    x["created_at"]
                                ),
                            ),
                        }
                    )
                    progress_counter.update(1)
            write_post(args, post_code, ret_data)

        if post_code != args.post_codes[-1]:
            for _ in tqdm(range(args.wait)):
                time.sleep(1)


def add_parse_post_cmd(parser: argparse.ArgumentParser) -> CommandFunction:
    """Add arbiter-command arguments to its parser."""
    parser.add_argument(
        "post_codes", nargs="+", help="Post codes to parse", type=str
    )
    parser.add_argument("-u", "--username", type=str)
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path("."),
        help="Path to output comments from posts",
    )
    parser.add_argument(
        "-P", "--prefix", help="Output file prefix", default=""
    )
    parser.add_argument(
        "-w",
        "--wait",
        type=int,
        default=60,
        help="Place a wait between parsing posts",
    )
    return parse_post_cmd
