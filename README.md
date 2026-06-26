# leetcode-lab

Personal LeetCode solutions with a built-in TypeScript debugger and automated task scaffolding.

## Structure

```bash
solutions/
├── Array/   # 16 problems
├── Linked List/   # 1 problems
├── Math/   # 2 problems
├── Tree/   # 1 problems
├── Two Pointers/   # 6 problems
└── Untagged/   # 19 problems
```

Files are named as `NNNN-problem-name.ts` and grouped by topic.

## Debugging

Two launch configurations in `.vscode/launch.json`:

| Configuration                        | What it does                                                            |
| ------------------------------------ | ----------------------------------------------------------------------- |
| **Debug TSX: Current File**          | Runs current `.ts` file with `--inspect-brk`, stops at breakpoints (F5) |
| **Run TSX: Current File (no debug)** | Runs current `.ts` file immediately (Ctrl+F5)                           |

Open any `.ts` file, set a breakpoint with F9, press F5.

## Adding a New Task

### From a LeetCode link

Use the `leetcode-skeleton.md` skill — send a LeetCode URL and it generates a TypeScript skeleton with the problem statement, signature, and examples ready to solve.

### Manually

1. Create `solutions/<Topic>/NNNN-problem-name.ts` with the task number prefix
2. Run the classification script to organize it by topic

## Classification Script

`scripts/reclassify.py` classifies problems by topic using LeetCode GraphQL API:

```bash
# Classify by topic (moves files into topic subdirectories)
python3 scripts/reclassify.py

# For a specific directory
python3 scripts/reclassify.py --dir solutions/custom
```

## Tasks

Total: 45 problems

### Array (16 files)

| # | Title | Difficulty |
|---|-------|------------|
| 150 | Evaluate Reverse Polish Notation | Medium |
| 268 | Missing Number | Easy |
| 283 | Move Zeroes | Easy |
| 448 | Find All Numbers Disappeared in an Array | Easy |
| 485 | Max Consecutive Ones | Easy |
| 605 | Can Place Flowers | Easy |
| 636 | Exclusive Time of Functions | Medium |
| 643 | Maximum Average Subarray I | Easy |
| 645 | Set Mismatch | Easy |
| 739 | Daily Temperatures | Medium |
| 977 | Squares of a Sorted Array | Easy |
| 1365 | How Many Numbers Are Smaller Than the Current Number | Easy |
| 1431 | Kids With the Greatest Number of Candies | Easy |
| 1441 | Build an Array With Stack Operations | Medium |
| 1470 | Shuffle the Array | Easy |
| 1475 | Final Prices With a Special Discount in a Shop | Easy |

### Linked List (1 files)

| # | Title | Difficulty |
|---|-------|------------|
| 206 | Reverse Linked List | Easy |

### Math (2 files)

| # | Title | Difficulty |
|---|-------|------------|
| 67 | Add Binary | Easy |
| 1071 | Greatest Common Divisor of Strings | Easy |

### Tree (1 files)

| # | Title | Difficulty |
|---|-------|------------|
| 104 | Maximum Depth of Binary Tree | Easy |

### Two Pointers (6 files)

| # | Title | Difficulty |
|---|-------|------------|
| 125 | Valid Palindrome | Easy |
| 151 | Reverse Words in a String | Medium |
| 345 | Reverse Vowels of a String | Easy |
| 392 | Is Subsequence | Easy |
| 844 | Backspace String Compare | Easy |
| 1768 | Merge Strings Alternately | Easy |

### Untagged (19 files)

| # | Title | Difficulty |
|---|-------|------------|
| 2620 | Counter | Easy |
| 2622 | Cache With Time Limit | Medium |
| 2623 | Memoize | Medium |
| 2626 | Array Reduce Transformation | Easy |
| 2627 | Debounce | Medium |
| 2629 | Function Composition | Easy |
| 2631 | Group By | Medium |
| 2637 | Promise Time Limit | Medium |
| 2665 | Counter II | Easy |
| 2666 | Allow One Function Call | Easy |
| 2677 | Chunk Array | Easy |
| 2693 | Call Function with Custom Context | Medium |
| 2703 | Return Length of Arguments Passed | Easy |
| 2715 | Timeout Cancellation | Easy |
| 2721 | Execute Asynchronous Functions in Parallel | Medium |
| 2723 | Add Two Promises | Easy |
| 2724 | Sort By | Easy |
| 2725 | Interval Cancellation | Easy |
| 2726 | Calculator with Method Chaining | Easy |

## Customization

### Other languages

The skeleton skill (`leetcode-skeleton.md`) targets TypeScript by default. To adapt for another language:

1. Edit the `## TypeScript Style` section in `leetcode-skeleton.md`
2. Replace function/class signatures with the target language's LeetCode starter code
3. Update `launch.json` for the language's debugger
