from typing import Iterator

from gogettr.capabilities.base import Capability
from gogettr.utils import merge


class Trends(Capability):
    def pull(
        self, max: int = None, until: str = None, lang: str = "en"
    ) -> Iterator[dict]:
        """Pull the current Gettr trends. This corresponds to the posts on the homepage.

        :param int max: the maximum number of posts to pull
        :param str until: the earliest post ID to pull
        :param str lang: the language of the trends (default `en`)"""

        url = "/u/posts/trends"
        n = 0

        for data in self.client.get_paginated(
            url,
            params={
                "lang": lang,
                "incl": "posts|stats|userinfo|shared|liked",
                "max": 20,
            },
        ):
            for post in data["data"]["list"]:
                id = post["activity"]["tgt_id"]

                # Information about posts is spread across four objects, so we merge them together here.
                post = merge(
                    post,
                    data["aux"]["post"].get(id),
                    data["aux"]["s_pst"].get(id),
                    {"uinf": data["aux"]["uinf"].get(post["activity"]["tgt_oid"])},
                )

                # Verify that we haven't passed the `until` post
                if until is not None and until > id:
                    return

                # Verify that we haven't passed the max number of posts
                if max is not None and n >= max:
                    return

                n += 1
                yield post
