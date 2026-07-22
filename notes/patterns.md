# Patterns

A cheat sheet for interview review (30–60 minutes). One pattern = one section: idea, code template, canonical problems from this repo and outside it.

Maintained via the `leetcode-practice` skill methodology — updated after each session where a pattern was worked through consciously (not just "solved the problem", but understood the general template).

## Two Pointers

**Idea:** two indices move across a structure toward each other or in the same direction to avoid nested iteration.

**Template:**
```ts
let left = 0
let right = arr.length - 1
while (left < right) {
  // check/decide using arr[left], arr[right]
  // move left++ and/or right--
}
```

**Problems in repo:**
- `solutions/Array/11-container-with-most-water.ts`
- `solutions/Array/15-3sum.ts`
- `solutions/Two Pointers/125-valid-palindrome.ts`
- `solutions/Two Pointers/151-reverse-words-in-a-string.ts`
- `solutions/Two Pointers/1768-merge-strings-alternately.ts`
- `solutions/Two Pointers/345-reverse-vowels-of-a-string.ts`
- `solutions/Two Pointers/392-is-subsequence.ts`
- `solutions/Two Pointers/844-backspace-string-compare.ts`

## Sliding Window

**Idea:** a window `[left, right]` expands/shrinks over the array/string, incrementally recalculating state instead of a full recompute on every step.

**Template:**
```ts
let left = 0
let state = 0 // sum/counter/set within the window
for (let right = 0; right < arr.length; right++) {
  // add arr[right] to state
  while (/* window invalid */) {
    // remove arr[left] from state
    left++
  }
  // update answer based on the current window
}
```

**Problems in repo:**
- `solutions/Array/643-maximum-average-subarray-i.ts`

## Monotonic Stack

**Idea:** the stack holds indices/values in monotonic order; an element gets popped once its "next greater/smaller" is found — amortized O(n) instead of O(n²).

**Template:**
```ts
const stack: number[] = [] // indices
const answer = new Array(arr.length).fill(0)
for (let i = 0; i < arr.length; i++) {
  while (stack.length && arr[i] > arr[stack.at(-1)!]) {
    const idx = stack.pop()!
    answer[idx] = i - idx
  }
  stack.push(i)
}
```

**Problems in repo:**
- `solutions/Array/739-daily-temperatures.ts`
- `solutions/Stack/155-min-stack.ts`
- `solutions/String/20-valid-parentheses.ts`
- `solutions/Array/1441-build-an-array-with-stack-operations.ts`
- `solutions/Array/853-car-fleet.ts` — same invariant without an explicit stack: walk from the car closest to the target toward the farthest, keeping a single number — the arrival time of the current leading fleet; if the new car's currentTime is greater than it, that's a new fleet.
- `solutions/Array/496-next-greater-element-i.ts` — same idea as Daily Temperatures, but instead of an index array the answer is written into a `Record`/`Map` (number → its next greater), because the final answer is needed not by position in the original array, but by value from a different array (nums1 is a subset of nums2). ([LeetCode](https://leetcode.com/problems/next-greater-element-i/), [NeetCode walkthrough](https://neetcode.io/solutions/next-greater-element-i))
- `solutions/Array/735-asteroid-collision.ts` — a "stack simulation with chain reaction" variant: an incoming negative element can destroy several elements at the top of the stack in a row, not just one. The key trap is not pushing `curr` right after its first win inside the `while` (otherwise `curr` becomes the new top and the loop stops early, never reaching elements deeper down). This needs an explicit "is curr still alive" flag (rather than checking the stack's shape afterward — a tie that empties the stack is indistinguishable, by the stack's final state, from a clean win that also empties it).

## Hash Map / Frequency Counting

**Idea:** trade O(n) memory for an O(1) check of "have we seen this", "how many times", "is there a pair matching the needed sum".

**Problems in repo:**
- `solutions/Array/49-group-anagrams.ts`
- `solutions/Array/128-longest-consecutive-sequence.ts`
- `solutions/Array/217-contains-duplicate.ts`
- `solutions/Array/347-top-k-frequent-elements.ts`
- `solutions/Hash Table/242-valid-anagram.ts`

## Binary Search

**Idea:** the answer space is monotonic — you can halve it instead of scanning linearly.

**Template:**
```ts
let lo = 0
let hi = arr.length - 1
while (lo <= hi) {
  const mid = lo + Math.floor((hi - lo) / 2)
  if (/* condition met */) return mid
  else if (/* need to go right */) lo = mid + 1
  else hi = mid - 1
}
```

**Problems in repo:** none yet — next target.

## Dynamic Programming

**Idea:** break the problem into overlapping subproblems, caching the result by invariant (index, remainder, bitmask, etc.).

**Problems in repo:** none yet — next target.

## Union-Find (DSU)

**Idea:** tracking connected components with near-O(1) union/find via path compression + union by rank.

**Problems in repo:** none yet.

## Graph BFS/DFS, Dijkstra

**Idea:** BFS — shortest path in an unweighted graph; Dijkstra — shortest path in a weighted graph with non-negative weights (priority queue).

**Problems in repo:** none yet.

---

## How to maintain this

1. After a `leetcode-practice` session, if a new pattern was worked through — add a section or extend an existing one: idea in 1-2 sentences, a minimal code template, a link to the solved problem.
2. Don't copy the full solution — only the generalized pattern template.
3. Keep "Problems in repo" current: the path must exist in `solutions/`.
