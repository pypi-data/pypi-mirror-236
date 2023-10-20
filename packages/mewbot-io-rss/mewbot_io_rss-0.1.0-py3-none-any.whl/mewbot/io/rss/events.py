# SPDX-FileCopyrightText: 2023 Mewbot Developers <mewbot@quicksilver.london>
#
# SPDX-License-Identifier: MIT

"""
Events which your IOConfig can produce/consume.
"""


from __future__ import annotations

import dataclasses

import feedparser  # type: ignore
from mewbot.api.v1 import InputEvent


@dataclasses.dataclass
class RSSInputEvent(InputEvent):
    """
    Should contain all the info from the original RSS message in a mewbot InputEvent.

    Some normalisation might be required, as not all RSS feeds seem to correspond to the standard.
    Spec from https://validator.w3.org/feed/docs/rss2.html#hrelementsOfLtitemgt
    """

    # pylint: disable=too-many-instance-attributes
    # Want to fully represent the core RSS standard

    title: str  # The title of the item.
    link: str  # The URL of the item.
    description: str  # The item synopsis.
    author: str  # Email address of the author of the item
    category: str  # Includes the item in one or more categories.
    comments: str  # URL of a page for comments relating to the item
    enclosure: str  # Optional URL of media associated with the file
    guid: str  # A unique identifier for the item
    pub_date: str  # Indicates when the item was published.
    source: str  # The RSS channel that the item came from.

    site_url: str  # The site according to us
    entry: feedparser.util.FeedParserDict  # raw entry for later processing

    startup: bool  # Was this feed read as part of first read for any given site?
