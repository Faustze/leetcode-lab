# leetcode-lab

Personal LeetCode solutions with a built-in TypeScript debugger and automated task scaffolding.

## Structure

```bash
solutions/
├── easy/            # 23 problems
├── medium/            # 10 problems
└── by-topic/        # 17 topic folders
```

Files are named as `NNNN-problem-name.ts` and grouped by difficulty and topic automatically.

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

1. Create `solutions/NNNN-problem-name.ts` with the task number prefix
2. Run the classification script to organize it

## Classification Script

Single script `scripts/reclassify.py` handles both difficulty and topic classification:

```bash
# Classify by difficulty (moves files into easy/medium/hard/)
python3 scripts/reclassify.py --difficulty

# Classify by topic (creates by-topic/ with symlinks)
python3 scripts/reclassify.py --topic

# Both at once
python3 scripts/reclassify.py --all

# For a specific directory
python3 scripts/reclassify.py --topic --dir solutions/custom
```

> **Note:** `by-topic/` is in `.gitignore` — it's regenerated locally and not committed.

## Tasks

Total: 33 problems

### easy (23 files)

| #    | Title                                                | Difficulty |
| ---- | ---------------------------------------------------- | ---------- |
| 104  | Maximum Depth of Binary Tree                         | ?          |
| 345  | Reverse Vowels of a String                           | ?          |
| 448  | Find All Numbers Disappeared in an Array             | ?          |
| 485  | Max Consecutive Ones                                 | ?          |
| 605  | Can Place Flowers                                    | ?          |
| 645  | Set Mismatch                                         | ?          |
| 1071 | Greatest Common Divisor of Strings                   | ?          |
| 1365 | How Many Numbers Are Smaller Than the Current Number | ?          |
| 1431 | Kids With the Greatest Number of Candies             | ?          |
| 1470 | Shuffle the Array                                    | ?          |
| 1768 | Merge Strings Alternately                            | ?          |
| 2620 | Counter                                              | ?          |
| 2626 | Array Reduce Transformation                          | ?          |
| 2629 | Function Composition                                 | ?          |
| 2665 | Counter II                                           | ?          |
| 2666 | Allow One Function Call                              | ?          |
| 2677 | Chunk Array                                          | ?          |
| 2703 | Return Length of Arguments Passed                    | ?          |
| 2715 | Timeout Cancellation                                 | ?          |
| 2723 | Add Two Promises                                     | ?          |
| 2724 | Sort By                                              | ?          |
| 2725 | Interval Cancellation                                | ?          |
| 2726 | Calculator with Method Chaining                      | ?          |

### medium (10 files)

| #    | Title                                      | Difficulty |
| ---- | ------------------------------------------ | ---------- |
| 150  | Evaluate Reverse Polish Notation           | ?          |
| 636  | Exclusive Time of Functions                | ?          |
| 1441 | Build an Array With Stack Operations       | ?          |
| 2622 | Cache With Time Limit                      | ?          |
| 2623 | Memoize                                    | ?          |
| 2627 | Debounce                                   | ?          |
| 2631 | Group By                                   | ?          |
| 2637 | Promise Time Limit                         | ?          |
| 2693 | Call Function with Custom Context          | ?          |
| 2721 | Execute Asynchronous Functions in Parallel | ?          |

## Customization

### Other languages

The skeleton skill (`leetcode-skeleton.md`) targets TypeScript by default. To adapt for another language:

1. Edit the `## TypeScript Style` section in `leetcode-skeleton.md`
2. Replace function/class signatures with the target language's LeetCode starter code
3. Update `launch.json` for the language's debugger
