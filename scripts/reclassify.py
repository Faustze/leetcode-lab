#!/usr/bin/env python3
"""
Reclassify LeetCode problems by difficulty and/or topic.

Usage:
    python3 scripts/reclassify.py                    # classify solutions/ by difficulty
    python3 scripts/reclassify.py --topic            # classify solutions/ by topic
    python3 scripts/reclassify.py --dir solutions/custom   # classify a specific dir
    python3 scripts/reclassify.py --topic --dir solutions/custom
    python3 scripts/reclassify.py --all              # difficulty + topic for solutions/
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
API_URL = "https://leetcode.com/api/problems/all/"


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def _fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def fetch_difficulty_map():
    """Return {frontend_question_id: 1|2|3} from LeetCode REST API."""
    data = _fetch_json(API_URL)
    result = {}
    for item in data.get("stat_status_pairs", []):
        stat = item.get("stat", {})
        qid = stat.get("frontend_question_id")
        level = item.get("difficulty", {}).get("level")
        if qid is not None and level is not None:
            result[qid] = level
    return result


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

def discover_ts_files(directory, recursive=True):
    """Return list of (absolute_path, filename) for all .ts files in directory."""
    results = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            # Skip by-topic (symlinks) and node_modules
            dirs[:] = [d for d in dirs if d not in ("by-topic", "node_modules", ".git")]
            for f in sorted(files):
                if f.endswith(".ts"):
                    results.append((os.path.join(root, f), f))
    else:
        for entry in sorted(os.listdir(directory)):
            if entry.endswith(".ts"):
                results.append((os.path.join(directory, entry), entry))
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
# Classification by difficulty
# ---------------------------------------------------------------------------

def classify_by_difficulty(directory, difficulty_map):
    """Move .ts files into easy/medium/hard/ subdirectories."""
    level_names = {1: "easy", 2: "medium", 3: "hard"}
    moved = {"easy": [], "medium": [], "hard": [], "unknown": []}

    for level_name in level_names.values():
        os.makedirs(os.path.join(directory, level_name), exist_ok=True)

    for filepath, filename in discover_ts_files(directory, recursive=False):
        num = extract_number(filename)
        if num is None:
            print(f"  SKIP: {filename} (no problem number prefix, expected NNNN-name.ts)")
            continue
        level = difficulty_map.get(num)
        dest_name = level_names.get(level)
        if dest_name is None:
            moved["unknown"].append(filename)
            continue
        dest = os.path.join(directory, dest_name, filename)
        if os.path.abspath(filepath) != os.path.abspath(dest):
            shutil.move(filepath, dest)
            moved[dest_name].append(filename)
            print(f"  {filename} -> {dest_name}/")

    return moved


# ---------------------------------------------------------------------------
# Classification by topic
# ---------------------------------------------------------------------------

def classify_by_topic(directory, topic_map, include_untagged=True):
    """Create by-topic/ with symlinks grouped by topic tag."""
    by_topic_dir = os.path.join(directory, "by-topic")
    os.makedirs(by_topic_dir, exist_ok=True)

    # Clean existing symlinks
    if os.path.exists(by_topic_dir):
        shutil.rmtree(by_topic_dir)
    os.makedirs(by_topic_dir)

    tagged = set()
    untagged = []

    for filepath, filename in discover_ts_files(directory):
        slug = extract_slug(filename)
        tags = topic_map.get(slug, [])

        if not tags and include_untagged:
            untagged.append(filename)

        for tag in tags:
            tag_dir = os.path.join(by_topic_dir, tag)
            os.makedirs(tag_dir, exist_ok=True)
            link = os.path.join(tag_dir, filename)
            if not os.path.exists(link):
                os.symlink(filepath, link)
            tagged.add(filename)

    if untagged:
        untagged_dir = os.path.join(by_topic_dir, "Untagged")
        os.makedirs(untagged_dir, exist_ok=True)
        for filename in untagged:
            link = os.path.join(untagged_dir, filename)
            if not os.path.exists(link):
                # Find the actual file
                for root, dirs, files in os.walk(directory):
                    if filename in files:
                        os.symlink(os.path.join(root, filename), link)
                        break

    print(f"  Tagged: {len(tagged)}, Untagged: {len(untagged)}")
    print(f"  Topics: {len(topic_map)} slugs resolved")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Reclassify LeetCode problems")
    parser.add_argument("--topic", action="store_true", help="Classify by topic (GraphQL API)")
    parser.add_argument("--difficulty", action="store_true", help="Classify by difficulty (REST API)")
    parser.add_argument("--dir", default=None, help="Target directory (default: src/leetcode)")
    parser.add_argument("--all", action="store_true", help="Both difficulty and topic")
    args = parser.parse_args()

    if not args.topic and not args.difficulty and not args.all:
        args.all = True  # default

    target_dir = args.dir or os.path.join(REPO_ROOT, "solutions")
    target_dir = os.path.abspath(target_dir)

    if not os.path.isdir(target_dir):
        print(f"Error: directory not found: {target_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Target: {target_dir}\n")

    if args.difficulty or args.all:
        print("=== Classification by difficulty ===")
        difficulty_map = fetch_difficulty_map()
        moved = classify_by_difficulty(target_dir, difficulty_map)
        for key, files in moved.items():
            print(f"  {key}: {len(files)} files")
        print()

    if args.topic or args.all:
        print("=== Classification by topic ===")
        slugs = []
        for _, filename in discover_ts_files(target_dir):
            slugs.append(extract_slug(filename))
        topic_map = fetch_topic_map(slugs)
        classify_by_topic(target_dir, topic_map)
        print()


if __name__ == "__main__":
    main()
