#!/usr/bin/env python3
"""
Sync generated markdown docs from leetcode-lab/md into the Obsidian vault.

Mirrors md/<Topic>/<file>.md into <vault>/public/leetcode/<Topic>/<file>.md.
Topics get matched by filename anywhere under public/leetcode (not just same
path), so a renamed/misfiled topic folder (e.g. old "Binary Tree" -> "Tree")
still finds its previous counterpart. Anything a human appended by hand after
the last closing code fence in the existing destination file (cross-links,
tags) is preserved and carried over to the new location.

Regenerates per-topic and top-level index.md navigation files from scratch
every run - those are pure listings, safe to rebuild. RESERVED_DIRS are never
read, written, or deleted.

Usage:
    python3 scripts/sync_vault.py
"""
import os
import re
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(REPO_ROOT, "md")
DEST_DIR = os.path.expanduser("~/OBSIDIAN/Obsidian-Notes/public/leetcode")
PRESERVED_DIRS = {"RegExp", "Patterns"}


def match_key(filename):
    """Match by problem number + slug, ignoring zero-padding differences
    (e.g. "49-group-anagrams.md" and "0049-group-anagrams.md" are the same
    problem)."""
    m = re.match(r"^0*(\d+)-(.*)$", filename)
    if not m:
        return filename
    number, rest = m.groups()
    return f"{number}-{rest}"


def extract_manual_footer(content):
    """Everything after the last closing ``` fence is treated as hand-added."""
    lines = content.split("\n")
    last_fence = -1
    for i, line in enumerate(lines):
        if line.strip() == "```":
            last_fence = i
    if last_fence == -1:
        return ""
    return "\n".join(lines[last_fence + 1:]).strip("\n")


def extract_inline_comments(content):
    """HTML comments hand-inserted inside the body (before the last fence),
    e.g. prev/next links dropped inside the examples block. Each is paired
    with the next non-blank line as an anchor, so it can be re-inserted at
    the same spot once the body is refreshed from a fresh source file."""
    lines = content.split("\n")
    last_fence = -1
    for i, line in enumerate(lines):
        if line.strip() == "```":
            last_fence = i
    body_end = last_fence if last_fence != -1 else len(lines)
    results = []
    for i, line in enumerate(lines[:body_end]):
        stripped = line.strip()
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            anchor = None
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    anchor = lines[j]
                    break
            results.append((line, anchor))
    return results


def reinsert_inline_comments(content, inline_comments):
    """Put hand-inserted HTML comments back at their anchor line. Returns
    (new_content, orphaned_comments) - orphaned ones couldn't find their
    anchor (body changed too much) and need a human to place them."""
    if not inline_comments:
        return content, []
    lines = content.split("\n")
    orphaned = []
    for comment_line, anchor in inline_comments:
        if comment_line in content:
            continue
        if anchor is None or anchor not in lines:
            orphaned.append(comment_line)
            continue
        lines.insert(lines.index(anchor), comment_line)
    return "\n".join(lines), orphaned


def index_existing_files(dest_dir):
    """filename -> (path, manual_footer, inline_comments) for every problem
    .md under dest_dir."""
    existing = {}
    for root, dirs, files in os.walk(dest_dir):
        if root == dest_dir:
            dirs[:] = [d for d in dirs if d not in PRESERVED_DIRS]
        for f in files:
            if f == "index.md" or not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            existing[match_key(f)] = (
                path,
                extract_manual_footer(content),
                extract_inline_comments(content),
            )
    return existing


def build_topic_index(topic, filenames):
    lines = [
        "---",
        f"title: {topic.lower()}",
        "---",
        "",
        f"# {topic}",
        "",
        "[[leetcode/index|← LeetCode]]",
        "",
    ]
    for fn in sorted(filenames):
        lines.append(f"- [[{topic}/{fn[:-3]}]]")
    lines.append("")
    lines.append("#leetcode")
    return "\n".join(lines)


def build_top_index(topics):
    lines = ["---", "title: leetcode", "---", "", "# LeetCode", ""]
    for t in sorted(topics):
        lines.append(f"- [[leetcode/{t}/index|{t}]]")
    lines.append("")
    lines.append("#leetcode")
    return "\n".join(lines)


def sync():
    if not os.path.isdir(DEST_DIR):
        raise SystemExit(f"Vault dir not found: {DEST_DIR}")

    existing = index_existing_files(DEST_DIR)
    source_topics = sorted(
        d for d in os.listdir(SOURCE_DIR)
        if os.path.isdir(os.path.join(SOURCE_DIR, d))
    )

    # Drop dest topic dirs that no longer exist in source (renames, cleanups).
    for entry in os.listdir(DEST_DIR):
        full = os.path.join(DEST_DIR, entry)
        if os.path.isdir(full) and entry not in PRESERVED_DIRS and entry not in source_topics:
            shutil.rmtree(full)
            print(f"  removed stale topic dir: {entry}")

    written = 0
    kept_footers = []
    orphaned_report = []

    for topic in source_topics:
        src_topic_dir = os.path.join(SOURCE_DIR, topic)
        dest_topic_dir = os.path.join(DEST_DIR, topic)
        os.makedirs(dest_topic_dir, exist_ok=True)

        filenames = sorted(f for f in os.listdir(src_topic_dir) if f.endswith(".md"))

        for fn in filenames:
            with open(os.path.join(src_topic_dir, fn)) as fh:
                content = fh.read().rstrip("\n")

            footer = ""
            key = match_key(fn)
            if key in existing:
                old_path, footer, inline_comments = existing[key]
                new_path = os.path.join(dest_topic_dir, fn)
                if os.path.normpath(old_path) != os.path.normpath(new_path) and os.path.exists(old_path):
                    os.remove(old_path)
                content, orphaned = reinsert_inline_comments(content, inline_comments)
                if orphaned:
                    orphaned_report.append((f"{topic}/{fn}", orphaned))

            if footer:
                content = content + "\n\n" + footer
                kept_footers.append(f"{topic}/{fn}")

            if "#leetcode" not in content:
                content = content + "\n#leetcode"

            with open(os.path.join(dest_topic_dir, fn), "w") as fh:
                fh.write(content + "\n")
            written += 1

        for stale_fn in os.listdir(dest_topic_dir):
            if stale_fn != "index.md" and stale_fn not in filenames:
                os.remove(os.path.join(dest_topic_dir, stale_fn))
                print(f"  removed stale file: {topic}/{stale_fn}")

        with open(os.path.join(dest_topic_dir, "index.md"), "w") as fh:
            fh.write(build_topic_index(topic, filenames) + "\n")

    all_topics = list(source_topics) + [
        d for d in PRESERVED_DIRS if os.path.isdir(os.path.join(DEST_DIR, d))
    ]
    with open(os.path.join(DEST_DIR, "index.md"), "w") as fh:
        fh.write(build_top_index(all_topics) + "\n")

    print(f"\n  Synced {written} files into {DEST_DIR}")
    if kept_footers:
        print(f"  Preserved manual footer in {len(kept_footers)} files:")
        for f in kept_footers:
            print(f"    - {f}")
    if orphaned_report:
        print(f"  WARNING: could not re-anchor inline comment(s) in {len(orphaned_report)} file(s) - place these by hand:")
        for f, comments in orphaned_report:
            print(f"    - {f}")
            for c in comments:
                print(f"        {c}")


if __name__ == "__main__":
    sync()
