#!/usr/bin/env python3
"""
Generate markdown documentation from TypeScript solution files.

Creates a mirrored directory structure under `md/` with .md files
containing the problem statement, code, and examples.

Usage:
    python3 scripts/generate_md.py          # generate md/ folder
    python3 scripts/generate_md.py --dry-run  # print one file to stdout
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLUTIONS_DIR = os.path.join(REPO_ROOT, "solutions")
MD_DIR = os.path.join(REPO_ROOT, "md")


def parse_ts_file(content):
    """Parse a .ts solution file into structured sections."""
    lines = content.split('\n')

    # Extract header: NNNN. Title (Difficulty) (URL) or NNNN. Title (URL)
    # Supports both // and /* */ comment formats
    title_match = None
    # Try with difficulty first
    m = re.search(r'(?://|/\*)\s*(\d+)\.\s*(.+?)\s*\((Easy|Medium|Hard)\)\s*\((https?://[^\)]+)\)', content)
    if m:
        title_match = m
    else:
        # Try without difficulty
        m2 = re.search(r'(?://|/\*)\s*(\d+)\.\s*(.+?)\s*\((https?://[^\)]+)\)', content)
        if m2:
            class MatchWithDiff:
                def __init__(self, match):
                    self._m = match
                def group(self, n):
                    if n == 3:
                        return None
                    elif n == 4:
                        return self._m.group(3)
                    return self._m.group(n)
            title_match = MatchWithDiff(m2)

    if not title_match:
        return None

    number = title_match.group(1)
    title = title_match.group(2).strip()
    difficulty = title_match.group(3) or "?"
    url = title_match.group(4)

    # Extract description (block comment before function/class)
    # Two formats:
    # 1. Header in //, description in separate /* ... */
    # 2. Header and description in same /* ... */
    description = ""
    in_desc = False
    desc_lines = []

    for line in lines:
        stripped = line.strip()
        # Check if this is the start of a block comment
        if not in_desc and stripped.startswith('/*'):
            in_desc = True
            continue
        if in_desc:
            # Check for end of block
            if '*/' in stripped:
                in_desc = False
                break
            cleaned = re.sub(r'^\s*\*\s?', '', line)
            cleaned = cleaned.strip()
            if not cleaned:
                continue
            desc_lines.append(cleaned)

    # Remove header line from description if present (NNNN. Title (Difficulty) (URL))
    if desc_lines and re.match(r'^\d+\.\s*.+?\s*\(.*\)\s*\(https?://', desc_lines[0]):
        desc_lines = desc_lines[1:]

    description = ' '.join(desc_lines).strip()

    # Extract code: from function/class declaration until we hit a line
    # that starts with '/*' (beginning of examples block) or end of file
    code_lines = []
    started = False

    for line in lines:
        stripped = line.strip()
        # Stop when we hit the examples block comment
        if started and stripped.startswith('/*'):
            break
        # Start capturing from function or class declaration
        if not started:
            if re.search(r'^(function|class|type|const|let|var)\s', stripped) or \
               re.search(r'^(export\s+)?(function|class)\s', stripped):
                started = True

        if started:
            code_lines.append(line)

    code = '\n'.join(code_lines).strip()

    # Extract examples (block comment after code)
    examples = ""
    last_block_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('/*'):
            last_block_start = i

    if last_block_start >= 0:
        example_lines = []
        in_block = False
        for i in range(last_block_start, len(lines)):
            line = lines[i]
            if line.strip().startswith('/*'):
                in_block = True
                continue
            if in_block:
                if line.strip().startswith('*/'):
                    break
                cleaned = re.sub(r'^\s*\*\s?', '', line)
                example_lines.append(cleaned.rstrip())
        examples = '\n'.join(example_lines).strip()

    return {
        "number": number,
        "title": title,
        "difficulty": difficulty,
        "url": url,
        "description": description,
        "code": code,
        "examples": examples,
    }


def generate_md(parsed):
    """Generate markdown content from parsed data."""
    if not parsed:
        return ""

    lines = []

    # Header - wrap URL in <> to avoid bare URL lint error
    lines.append(f"# {parsed['number']}. {parsed['title']} ({parsed['difficulty']}) (<{parsed['url']}>)")
    lines.append("")

    # Description - use blockquote to avoid ordered list lint issues
    if parsed['description']:
        desc = parsed['description']
        sentences = re.split(r'(?<=\.)\s+', desc)
        for sentence in sentences:
            if sentence.strip():
                lines.append(f"> {sentence.strip()}")
        lines.append("")

    # Code block with language specifier
    if parsed['code']:
        lines.append("```ts")
        lines.append(parsed['code'])
        lines.append("```")
        lines.append("")

    # Examples - use blockquote to avoid ordered list lint issues
    if parsed['examples']:
        lines.append("```md")
        lines.append(parsed['examples'])
        lines.append("```")
        lines.append("")

    return '\n'.join(lines)


def generate_all():
    """Generate md/ directory structure from solutions/."""
    if os.path.exists(MD_DIR):
        import shutil
        shutil.rmtree(MD_DIR)
    os.makedirs(MD_DIR, exist_ok=True)

    count = 0

    for topic in sorted(os.listdir(SOLUTIONS_DIR)):
        topic_path = os.path.join(SOLUTIONS_DIR, topic)
        if not os.path.isdir(topic_path) or topic.startswith('.'):
            continue

        md_topic_dir = os.path.join(MD_DIR, topic)
        os.makedirs(md_topic_dir, exist_ok=True)

        for filename in sorted(os.listdir(topic_path)):
            if not filename.endswith('.ts'):
                continue

            filepath = os.path.join(topic_path, filename)
            with open(filepath, 'r') as f:
                content = f.read()

            parsed = parse_ts_file(content)
            if not parsed:
                print(f"  Warning: could not parse {filename}", file=sys.stderr)
                continue

            md_content = generate_md(parsed)
            if not md_content:
                continue

            md_filename = filename.replace('.ts', '.md')
            md_filepath = os.path.join(md_topic_dir, md_filename)

            with open(md_filepath, 'w') as f:
                f.write(md_content)

            count += 1
            print(f"  {filename} -> md/{topic}/{md_filename}")

    print(f"\n  Generated {count} markdown files")


def dry_run():
    """Print one example to stdout."""
    for topic in sorted(os.listdir(SOLUTIONS_DIR)):
        topic_path = os.path.join(SOLUTIONS_DIR, topic)
        if not os.path.isdir(topic_path) or topic.startswith('.'):
            continue
        for filename in sorted(os.listdir(topic_path)):
            if not filename.endswith('.ts'):
                continue
            filepath = os.path.join(topic_path, filename)
            with open(filepath, 'r') as f:
                content = f.read()
            parsed = parse_ts_file(content)
            if parsed:
                md = generate_md(parsed)
                print(f"--- Preview for {topic}/{filename} ---\n")
                print(md)
                return


def main():
    dry_run_mode = "--dry-run" in sys.argv

    if dry_run_mode:
        dry_run()
    else:
        print("Generating markdown documentation...\n")
        generate_all()


if __name__ == "__main__":
    main()
