#!/usr/bin/env python3
"""
Reclassify LeetCode problems by topic.

Moves .ts files from solutions/ into solutions/<Topic>/ subdirectories
based on LeetCode GraphQL topic tags. Files already in subdirectories are also classified.

Usage:
    python3 scripts/reclassify.py                    # classify solutions/ by topic
    python3 scripts/reclassify.py --dir solutions/custom   # classify a specific dir
"""
import argparse
import json
import os
import re
import shutil
import sys
import time
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPHQL_URL = "https://leetcode.com/graphql"


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def fetch_topic_map(title_slugs):
    """Return {title_slug: [topic_names]} from LeetCode GraphQL API."""
    query = """
    query getQuestion($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            titleSlug
            topicTags { name }
        }
    }
    """
    result = {}
    for i, slug in enumerate(title_slugs):
        try:
            payload = json.dumps({"query": query, "variables": {"titleSlug": slug}}).encode()
            req = urllib.request.Request(
                GRAPHQL_URL,
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
            q = data.get("data", {}).get("question", {})
            if q:
                result[slug] = [t["name"] for t in q.get("topicTags", [])]
        except Exception as e:
            print(f"  Warning: {slug} failed: {e}", file=sys.stderr)
        if (i + 1) % 20 == 0:
            time.sleep(0.5)
    return result


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def discover_ts_files(directory):
    """Return list of (absolute_path, filename) for all .ts files in directory (recursive, skip topic dirs at root)."""
    results = []
    for root, dirs, files in os.walk(directory):
        # Skip topic directories at root level (they are classification targets)
        if root == directory:
            dirs[:] = []
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git")]
        for f in sorted(files):
            if f.endswith(".ts"):
                results.append((os.path.join(root, f), f))
    return results


def extract_number(filename):
    """Extract problem number from 'NNNN-name.ts'."""
    m = re.match(r"^(\d+)-", filename)
    return int(m.group(1)) if m else None


def extract_slug(filename):
    """Extract title slug from 'NNNN-name.ts' -> 'name'."""
    name = filename.replace(".ts", "")
    m = re.match(r"^\d+-(.+)$", name)
    return m.group(1) if m else name


# ---------------------------------------------------------------------------
# Classification by topic
# ---------------------------------------------------------------------------

def classify_by_topic(directory, topic_map):
    """Move .ts files into topic subdirectories grouped by topic tag."""
    # Collect all files and their topics
    files_to_classify = []

    for filepath, filename in discover_ts_files(directory):
        slug = extract_slug(filename)
        tags = topic_map.get(slug, [])
        primary_tag = tags[0] if tags else "Untagged"
        files_to_classify.append((filepath, filename, primary_tag))

    # Remove all existing topic directories (non-.ts dirs in root)
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)
        if os.path.isdir(entry_path) and not entry.startswith("."):
            shutil.rmtree(entry_path)

    # Move files to topic directories
    tagged = set()
    untagged = []

    for filepath, filename, tag in files_to_classify:
        tag_dir = os.path.join(directory, tag)
        os.makedirs(tag_dir, exist_ok=True)
        dest = os.path.join(tag_dir, filename)
        if os.path.abspath(filepath) != os.path.abspath(dest):
            shutil.move(filepath, dest)
            print(f"  {filename} -> {tag}/")
        tagged.add(filename)

    print(f"\n  Total: {len(files_to_classify)} files classified")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Reclassify LeetCode problems by topic")
    parser.add_argument("--dir", default=None, help="Target directory (default: solutions/)")
    args = parser.parse_args()

    target_dir = args.dir or os.path.join(REPO_ROOT, "solutions")
    target_dir = os.path.abspath(target_dir)

    if not os.path.isdir(target_dir):
        print(f"Error: directory not found: {target_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Target: {target_dir}\n")

    print("=== Classification by topic ===")
    slugs = []
    for _, filename in discover_ts_files(target_dir):
        slugs.append(extract_slug(filename))
    topic_map = fetch_topic_map(slugs)
    classify_by_topic(target_dir, topic_map)
    print()


if __name__ == "__main__":
    main()
