#!/usr/bin/env python3
"""
Update README.md based on current solutions/ directory structure.

Reads all .ts files, fetches problem metadata from LeetCode API,
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
        level = stat.get("difficulty", {}).get("level", 0)
        diff = {1: "Easy", 2: "Medium", 3: "Hard"}.get(level, "?")
        title = stat.get("question__title", "")
        info[qid] = {"title": title, "diff": diff}
    return info


def scan_solutions():
    """Scan solutions/ and return {subdir: [(num, filename, abs_path)]}."""
    results = {}
    for root, dirs, files in os.walk(SOLUTIONS_DIR):
        dirs[:] = [d for d in dirs if d not in ("by-topic", "node_modules", ".git")]
        for f in sorted(files):
            if not f.endswith(".ts"):
                continue
            m = re.match(r"^(\d+)-", f)
            if not m:
                continue
            num = int(m.group(1))
            subdir = os.path.relpath(root, SOLUTIONS_DIR)
            if subdir == ".":
                subdir = ""
            results.setdefault(subdir, []).append((num, f))
    return results


def count_files_by_extension(directory, ext=".ts"):
    """Count files with given extension recursively."""
    count = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ("by-topic", "node_modules", ".git")]
        count += sum(1 for f in files if f.endswith(ext))
    return count


def generate_readme(problem_info, solutions):
    """Generate README.md content."""
    total = sum(len(files) for files in solutions.values())

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

    # Build tree
    subdirs = sorted(solutions.keys())
    for i, subdir in enumerate(subdirs):
        is_last = i == len(subdir) - 1
        prefix = "└── " if is_last else "├── "
        count = len(solutions[subdir])
        lines.append(f"{prefix}{subdir}/            # {count} problems")

    # Check for by-topic
    by_topic_dir = os.path.join(SOLUTIONS_DIR, "by-topic")
    if os.path.isdir(by_topic_dir):
        topic_count = sum(1 for _ in os.listdir(by_topic_dir) if os.path.isdir(os.path.join(by_topic_dir, _)))
        lines.append(f"└── by-topic/        # {topic_count} topic folders")

    lines.append("```")
    lines.append("")
    lines.append("Files are named as `NNNN-problem-name.ts` and grouped by difficulty and topic automatically.")
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
    lines.append("1. Create `solutions/NNNN-problem-name.ts` with the task number prefix")
    lines.append("2. Run the classification script to organize it")
    lines.append("")

    # --- Classification Script ---
    lines.append("## Classification Script")
    lines.append("")
    lines.append("Single script `scripts/reclassify.py` handles both difficulty and topic classification:")
    lines.append("")
    lines.append("```bash")
    lines.append("# Classify by difficulty (moves files into easy/medium/hard/)")
    lines.append("python3 scripts/reclassify.py --difficulty")
    lines.append("")
    lines.append("# Classify by topic (creates by-topic/ with symlinks)")
    lines.append("python3 scripts/reclassify.py --topic")
    lines.append("")
    lines.append("# Both at once")
    lines.append("python3 scripts/reclassify.py --all")
    lines.append("")
    lines.append("# For a specific directory")
    lines.append("python3 scripts/reclassify.py --topic --dir solutions/leetcode-75")
    lines.append("```")
    lines.append("")
    lines.append("> **Note:** `by-topic/` is in `.gitignore` — it's regenerated locally and not committed.")
    lines.append("")

    # --- Tasks ---
    lines.append("## Tasks")
    lines.append("")
    lines.append(f"Total: {total} problems")
    lines.append("")

    for subdir in subdirs:
        files = solutions[subdir]
        label = subdir if subdir else "root"
        lines.append(f"### {label} ({len(files)} files)")
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
    solutions = scan_solutions()

    if not solutions:
        print("No .ts files found in solutions/", file=sys.stderr)
        sys.exit(1)

    total = sum(len(files) for files in solutions.values())
    print(f"Found {total} problems in {len(solutions)} groups")

    content = generate_readme(problem_info, solutions)

    if dry_run:
        print("\n--- README preview ---\n")
        print(content)
    else:
        with open(README_PATH, "w") as f:
            f.write(content)
        print(f"Updated {README_PATH}")


if __name__ == "__main__":
    main()
