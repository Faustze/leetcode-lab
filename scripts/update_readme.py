#!/usr/bin/env python3
"""
Update README.md based on current solutions/ directory structure.

Reads all .ts files from topic subdirectories, fetches problem metadata from LeetCode API,
and regenerates the entire README with correct paths, counts, and task tables.

Usage:
    python3 scripts/update_readme.py          # update README.md
    python3 scripts/update_readme.py --dry-run  # print to stdout instead
"""
import json
import os
import re
import sys
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLUTIONS_DIR = os.path.join(REPO_ROOT, "solutions")
README_PATH = os.path.join(REPO_ROOT, "README.md")
API_URL = "https://leetcode.com/api/problems/all/"


def fetch_problem_info():
    """Fetch {number: {title, difficulty}} from LeetCode REST API."""
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    info = {}
    for item in data.get("stat_status_pairs", []):
        stat = item.get("stat", {})
        qid = stat.get("frontend_question_id")
        if qid is None:
            continue
        level = item.get("difficulty", {}).get("level", 0)
        diff = {1: "Easy", 2: "Medium", 3: "Hard"}.get(level, "?")
        title = stat.get("question__title", "")
        info[qid] = {"title": title, "diff": diff}
    return info


def scan_solutions():
    """Scan solutions/ topic subdirectories and return {topic: [(num, filename)]}."""
    results = {}
    for entry in sorted(os.listdir(SOLUTIONS_DIR)):
        entry_path = os.path.join(SOLUTIONS_DIR, entry)
        if not os.path.isdir(entry_path) or entry.startswith("."):
            continue
        topic = entry
        for f in sorted(os.listdir(entry_path)):
            if not f.endswith(".ts"):
                continue
            m = re.match(r"^(\d+)-", f)
            if not m:
                continue
            num = int(m.group(1))
            results.setdefault(topic, []).append((num, f))
    return results


def generate_readme(problem_info, by_topic):
    """Generate README.md content."""
    total = sum(len(files) for files in by_topic.values())

    lines = []
    lines.append("# leetcode-lab")
    lines.append("")
    lines.append("Personal LeetCode solutions with a built-in TypeScript debugger and automated task scaffolding.")
    lines.append("")

    # --- Structure ---
    lines.append("## Structure")
    lines.append("")
    lines.append("```bash")
    lines.append("solutions/")

    topics = sorted(by_topic.keys())
    for i, topic in enumerate(topics):
        is_last = i == len(topics) - 1
        prefix = "└── " if is_last else "├── "
        count = len(by_topic[topic])
        lines.append(f"{prefix}{topic}/   # {count} problems")

    lines.append("```")
    lines.append("")
    lines.append("Files are named as `NNNN-problem-name.ts` and grouped by topic.")
    lines.append("")

    # --- Debugging ---
    lines.append("## Debugging")
    lines.append("")
    lines.append("Two launch configurations in `.vscode/launch.json`:")
    lines.append("")
    lines.append("| Configuration                        | What it does                                                            |")
    lines.append("| ------------------------------------ | ----------------------------------------------------------------------- |")
    lines.append("| **Debug TSX: Current File**          | Runs current `.ts` file with `--inspect-brk`, stops at breakpoints (F5) |")
    lines.append("| **Run TSX: Current File (no debug)** | Runs current `.ts` file immediately (Ctrl+F5)                           |")
    lines.append("")
    lines.append("Open any `.ts` file, set a breakpoint with F9, press F5.")
    lines.append("")

    # --- Adding a New Task ---
    lines.append("## Adding a New Task")
    lines.append("")
    lines.append("### From a LeetCode link")
    lines.append("")
    lines.append("Use the `leetcode-skeleton.md` skill — send a LeetCode URL and it generates a TypeScript skeleton with the problem statement, signature, and examples ready to solve.")
    lines.append("")
    lines.append("### Manually")
    lines.append("")
    lines.append("1. Create `solutions/<Topic>/NNNN-problem-name.ts` with the task number prefix")
    lines.append("2. Run the classification script to organize it by topic")
    lines.append("")

    # --- Classification Script ---
    lines.append("## Classification Script")
    lines.append("")
    lines.append("`scripts/reclassify.py` classifies problems by topic using LeetCode GraphQL API:")
    lines.append("")
    lines.append("```bash")
    lines.append("# Classify by topic (moves files into topic subdirectories)")
    lines.append("python3 scripts/reclassify.py")
    lines.append("")
    lines.append("# For a specific directory")
    lines.append("python3 scripts/reclassify.py --dir solutions/custom")
    lines.append("```")
    lines.append("")

    # --- Tasks ---
    lines.append("## Tasks")
    lines.append("")
    lines.append(f"Total: {total} problems")
    lines.append("")

    for topic in topics:
        files = by_topic[topic]
        lines.append(f"### {topic} ({len(files)} files)")
        lines.append("")
        lines.append("| # | Title | Difficulty |")
        lines.append("|---|-------|------------|")
        for num, fname in sorted(files, key=lambda x: x[0]):
            meta = problem_info.get(num, {})
            title = meta.get("title", fname.replace(".ts", ""))
            diff = meta.get("diff", "?")
            lines.append(f"| {num} | {title} | {diff} |")
        lines.append("")

    # --- Customization ---
    lines.append("## Customization")
    lines.append("")
    lines.append("### Other languages")
    lines.append("")
    lines.append("The skeleton skill (`leetcode-skeleton.md`) targets TypeScript by default. To adapt for another language:")
    lines.append("")
    lines.append("1. Edit the `## TypeScript Style` section in `leetcode-skeleton.md`")
    lines.append("2. Replace function/class signatures with the target language's LeetCode starter code")
    lines.append("3. Update `launch.json` for the language's debugger")

    return "\n".join(lines) + "\n"


def main():
    dry_run = "--dry-run" in sys.argv

    print("Fetching problem info from LeetCode API...")
    problem_info = fetch_problem_info()

    print("Scanning solutions/...")
    by_topic = scan_solutions()

    if not by_topic:
        print("No .ts files found in solutions/ topic subdirectories", file=sys.stderr)
        sys.exit(1)

    total = sum(len(files) for files in by_topic.values())
    print(f"Found {total} problems in {len(by_topic)} topics")

    content = generate_readme(problem_info, by_topic)

    if dry_run:
        print("\n--- README preview ---\n")
        print(content)
    else:
        with open(README_PATH, "w") as f:
            f.write(content)
        print(f"Updated {README_PATH}")


if __name__ == "__main__":
    main()
