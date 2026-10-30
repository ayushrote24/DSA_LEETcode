#!/usr/bin/env python3
"""Refresh README stats using LeetCode's public profile GraphQL query.

Only public profile statistics are requested. No session cookies or private
submission source code are used.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USERNAME = os.environ.get("LEETCODE_USERNAME", "ayushrote24")
README = "README.md"
START = "<!-- LEETCODE_STATS_START -->"
END = "<!-- LEETCODE_STATS_END -->"
QUERY = """
query userProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile { ranking }
    submitStats {
      acSubmissionNum { difficulty count }
    }
  }
}
"""

def fetch_stats() -> dict:
    payload = json.dumps({
        "query": QUERY,
        "variables": {"username": USERNAME},
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/{USERNAME}/",
            "User-Agent": "Mozilla/5.0 (compatible; LeetCodeDashboard/1.0)",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        result = json.loads(response.read().decode("utf-8"))
    if result.get("errors") or not result.get("data", {}).get("matchedUser"):
        raise RuntimeError("LeetCode did not return a public profile for this username.")
    return result["data"]["matchedUser"]

def render_stats(user: dict) -> str:
    counts = {row["difficulty"]: row["count"]
              for row in user["submitStats"]["acSubmissionNum"]}
    easy = counts.get("Easy", 0)
    medium = counts.get("Medium", 0)
    hard = counts.get("Hard", 0)
    total = counts.get("All", easy + medium + hard)
    ranking = user.get("profile", {}).get("ranking") or "—"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<div align="center">

| 🧩 Solved | 🟢 Easy | 🟡 Medium | 🔴 Hard | 🌍 Global rank |
|:---:|:---:|:---:|:---:|:---:|
| **{total}** | **{easy}** | **{medium}** | **{hard}** | **{ranking}** |

<sub>Last refreshed: {now} · Source: public LeetCode profile</sub>

</div>"""

def main() -> int:
    try:
        with open(README, "r", encoding="utf-8") as file:
            content = file.read()
        if START not in content or END not in content:
            raise RuntimeError("README statistics markers were not found.")
        stats = render_stats(fetch_stats())
        updated = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            lambda _: START + "\n" + stats + "\n" + END,
            content,
            count=1,
            flags=re.DOTALL,
        )
        if updated == content:
            print("README statistics are already current.")
            return 0
        with open(README, "w", encoding="utf-8") as file:
            file.write(updated)
        print("Updated README statistics successfully.")
        return 0
    except (OSError, urllib.error.URLError, TimeoutError, ValueError, RuntimeError) as exc:
        print(f"Dashboard update failed safely: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
