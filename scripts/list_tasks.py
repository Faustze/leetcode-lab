#!/usr/bin/env python3
"""Generate a task listing for README.md from LeetCode API data."""
import json
import os
import re
import sys
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_URL = "https://leetcode.com/api/problems/all/"


def main():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    # Build maps
    info = {}  # number -> {title, difficulty, slug}
    for item in data.get("stat_status_pairs", []):
        stat = item.get("stat", {})
        qid = stat.get("frontend_question_id")
        if qid is None:
            continue
        level = item.get("difficulty", {}).get("level", 0)
        diff = {1: "Easy", 2: "Medium", 3: "Hard"}.get(level, "?")
        title = stat.get("question__title", "")
        slug = stat.get("question__title_slug", "")
        info[qid] = {"title": title, "diff": diff, "slug": slug}

    # Scan all .ts files
    src_dir = os.path.join(REPO_ROOT, "src", "leetcode")
    files = []
    for root, dirs, fnames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ("by-topic", "node_modules")]
        for f in fnames:
            if f.endswith(".ts"):
                m = re.match(r"^(\d+)-(.+)\.ts$", f)
                if m:
                    num = int(m.group(1))
                    subdir = os.path.relpath(root, src_dir)
                    if subdir == ".":
                        subdir = ""
                    files.append((num, f, subdir))

    files.sort(key=lambda x: x[0])

    # Group by subdir
    groups = {}
    for num, fname, subdir in files:
        groups.setdefault(subdir, []).append((num, fname))

    lines = []
    lines.append(f"Total: {len(files)} problems\n")

    for subdir in sorted(groups.keys()):
        label = subdir if subdir else "root"
        lines.append(f"### {label} ({len(groups[subdir])} files)\n")
        lines.append("| # | Title | Difficulty |")
        lines.append("|---|-------|------------|")
        for num, fname in groups[subdir]:
            meta = info.get(num, {})
            title = meta.get("title", fname.replace(".ts", ""))
            diff = meta.get("diff", "?")
            lines.append(f"| {num} | {title} | {diff} |")
        lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
