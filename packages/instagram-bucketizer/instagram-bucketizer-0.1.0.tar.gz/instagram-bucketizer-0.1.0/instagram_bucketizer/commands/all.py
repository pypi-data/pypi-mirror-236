# =====================================
# generator=datazen
# version=3.1.4
# hash=8195916b986da0c0f4a634676fb6781b
# =====================================

"""
A module aggregating package commands.
"""

# built-in
from typing import List as _List
from typing import Tuple as _Tuple

# third-party
from vcorelib.args import CommandRegister as _CommandRegister

# internal
from instagram_bucketizer.commands.bucketize import add_bucketize_cmd
from instagram_bucketizer.commands.parse_post import add_parse_post_cmd
from instagram_bucketizer.commands.setup_session import add_setup_session_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "bucketize",
            "bucketize comments",
            add_bucketize_cmd,
        ),
        (
            "parse_post",
            "parse a given post short code",
            add_parse_post_cmd,
        ),
        (
            "setup_session",
            "Used firefox cookies to setup session file",
            add_setup_session_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
