"""
    Setup a session file based on web browser cookies
"""
# This command is a workaround for instaloader
# and thus contains some improper accesses etc..
# see https://instaloader.github.io/troubleshooting.html
# mypy: ignore-errors

# built-in
import argparse
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

from instaloader import ConnectionException, Instaloader

# third-party
from vcorelib.args import CommandFunction

WINDOWS_PATH = (
    "~/AppData/Roaming/" + "Mozilla/Firefox/Profiles/*/cookies.sqlite"
)
DARWIN_PATH = (
    "~/Library/Application Support/" + "Firefox/Profiles/*/cookies.sqlite"
)
LINUX_PATH = "~/.mozilla/firefox/*/" + "cookies.sqlite"


def get_cookiefile():
    """
    Find a cookie file
    """

    default_cookiefile = {
        "Windows": WINDOWS_PATH,
        "Darwin": DARWIN_PATH,
    }.get(system(), LINUX_PATH)
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit(
            "No Firefox cookies.sqlite file found. Use -c COOKIEFILE."
        )
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    """
    Save a session file
    """

    print(f"Using cookies from {cookiefile}.")
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies"
            + " WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies"
            + " WHERE host LIKE '%instagram.com'"
        )
    instaloader = Instaloader(max_connection_attempts=1)

    # this session setup is generally a workaround
    # pylint: disable=protected-access
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit(
            "Not logged in. Are you logged in successfully in Firefox?"
        )
    print(f"Imported session cookie for {username}.")
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)


def setup_session_cmd(args: argparse.Namespace):
    """
    Setup a session file command
    """

    try:
        import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
    except (ConnectionException, OperationalError) as e:
        raise SystemExit(f"Cookie import failed: {e}") from e


def add_setup_session_cmd(parser: argparse.ArgumentParser) -> CommandFunction:
    """Add arbiter-command arguments to its parser."""
    parser.add_argument("-c", "--cookiefile")
    parser.add_argument("-f", "--sessionfile")
    return setup_session_cmd
