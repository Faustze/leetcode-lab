# leetcode-lab

Personal LeetCode solutions with a built-in TypeScript debugger and automated task scaffolding.

## Structure

```bash
solutions/
├── Array/   # 14 problems
├── Math/   # 2 problems
├── Tree/   # 1 problems
├── Two Pointers/   # 4 problems
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
# Classify all problems by topic
python3 scripts/reclassify.py

# Classify a single problem by slug
python3 scripts/reclassify.py --file 1475-final-prices-with-a-special-discount-in-a-shop

# For a specific directory
python3 scripts/reclassify.py --dir solutions/custom
```

Or via npm:

```bash
# Classify a single problem
npm run classify -- <slug>
```

## Tasks

Total: 40 problems

### Array (14 files)

| #    | Title                                                | Difficulty |
| ---- | ---------------------------------------------------- | ---------- |
| 150  | Evaluate Reverse Polish Notation                     | ?          |
| 268  | Missing Number                                       | ?          |
| 283  | Move Zeroes                                          | ?          |
| 448  | Find All Numbers Disappeared in an Array             | ?          |
| 485  | Max Consecutive Ones                                 | ?          |
| 605  | Can Place Flowers                                    | ?          |
| 636  | Exclusive Time of Functions                          | ?          |
| 645  | Set Mismatch                                         | ?          |
| 739  | Daily Temperatures                                   | ?          |
| 1365 | How Many Numbers Are Smaller Than the Current Number | ?          |
| 1431 | Kids With the Greatest Number of Candies             | ?          |
| 1441 | Build an Array With Stack Operations                 | ?          |
| 1470 | Shuffle the Array                                    | ?          |
| 1475 | Final Prices With a Special Discount in a Shop       | ?          |

### Math (2 files)

| #    | Title                              | Difficulty |
| ---- | ---------------------------------- | ---------- |
| 67   | Add Binary                         | ?          |
| 1071 | Greatest Common Divisor of Strings | ?          |

### Tree (1 files)

| #   | Title                        | Difficulty |
| --- | ---------------------------- | ---------- |
| 104 | Maximum Depth of Binary Tree | ?          |

### Two Pointers (4 files)

| #    | Title                      | Difficulty |
| ---- | -------------------------- | ---------- |
| 125  | Valid Palindrome           | ?          |
| 151  | Reverse Words in a String  | ?          |
| 345  | Reverse Vowels of a String | ?          |
| 1768 | Merge Strings Alternately  | ?          |

### Untagged (19 files)

| #    | Title                                      | Difficulty |
| ---- | ------------------------------------------ | ---------- |
| 2620 | Counter                                    | ?          |
| 2622 | Cache With Time Limit                      | ?          |
| 2623 | Memoize                                    | ?          |
| 2626 | Array Reduce Transformation                | ?          |
| 2627 | Debounce                                   | ?          |
| 2629 | Function Composition                       | ?          |
| 2631 | Group By                                   | ?          |
| 2637 | Promise Time Limit                         | ?          |
| 2665 | Counter II                                 | ?          |
| 2666 | Allow One Function Call                    | ?          |
| 2677 | Chunk Array                                | ?          |
| 2693 | Call Function with Custom Context          | ?          |
| 2703 | Return Length of Arguments Passed          | ?          |
| 2715 | Timeout Cancellation                       | ?          |
| 2721 | Execute Asynchronous Functions in Parallel | ?          |
| 2723 | Add Two Promises                           | ?          |
| 2724 | Sort By                                    | ?          |
| 2725 | Interval Cancellation                      | ?          |
| 2726 | Calculator with Method Chaining            | ?          |

## Customization

### Other languages

The skeleton skill (`leetcode-skeleton.md`) targets TypeScript by default. To adapt for another language:

1. Edit the `## TypeScript Style` section in `leetcode-skeleton.md`
2. Replace function/class signatures with the target language's LeetCode starter code
3. Update `launch.json` for the language's debugger
