# LeetCode Skeleton Workflow

Use this when the user sends a LeetCode task link and asks to prepare a skeleton.
Always prepare the task in TypeScript.

## Goal

Create a TypeScript file that preserves the task statement and gives the user a clean place to solve it locally.
Use LeetCode's TypeScript language option for the exact starter code, function signature, class shape, method names, and starter types.

Use `solutions/easy/2723-add-two-promises.ts` as the style reference.

## Target File

- Put the file in `solutions/` (the root of the solutions directory).
- Name it with the problem number prefix followed by the kebab-case slug:
  - `https://leetcode.com/problems/memoize/` -> `2623-memoize.ts`
  - `https://leetcode.com/problems/allow-one-function-call/` -> `2666-allow-one-function-call.ts`
  - `https://leetcode.com/problems/daily-temperatures/` -> `739-daily-temperatures.ts`
- Format: `NNNN-problem-name.ts` (zero-padded number, dash, kebab-case slug).
- If a file already exists, update it only if the user clearly wants that.
- After creating, run `npm run update` to classify by difficulty and topic.

## File Shape

For the solution stub, copy the LeetCode TypeScript starter shape. If the task uses a function, keep the function form. If the task uses a class, keep the class form.

Function task:

```ts
// <number>. <Title> (<Difficulty>) (<url>)
/*
  <short original problem statement>

  <important constraints or behavior notes>
*/

type <TaskTypes> = <...>

function <expectedFunctionName>(<params>): <returnType> {
}
```

Class task:

```ts
// <number>. <Title> (<Difficulty>) (<url>)
/*
  <short original problem statement>

  <important constraints or behavior notes>
*/

class <ExpectedClassName> {
  constructor() {

  }

  <methodName>(<params>): <returnType> {

  }
}

/**
 * <LeetCode instantiation comment>
 */
```

Then add examples below:

```ts

// Local check:
console.log(<expectedFunctionName>(<example input 1>))
console.log(<expectedFunctionName>(<example input 2>))
console.log(<expectedFunctionName>(<example input 3>))

/*
  Example 1:

    Input: <...>
    Output: <...>
    Explanation: <...>

  Example 2:

    Input: <...>
    Output: <...>
    Explanation: <...>
*/
```

## Content Rules

- Keep the LeetCode title line as the first line.
- Preserve the problem number, title, difficulty, and URL.
- Copy or summarize the statement into a block comment.
- Include examples from the task page in the final block comment.
- Add `Local check` as executable code, directly under the solution stub:
  use `// Local check:` followed by `console.log(...)` calls, not a block comment.
- Add only the TypeScript starter code LeetCode gives for the task.
- Do not translate from C++, Java, Python, JavaScript, or any other language.
- Do not add C++-style `public`, `private`, semicolon-heavy class blocks, `nullptr`, `vector`, or other non-TypeScript syntax.
- Do not solve the task unless the user asks for a solution.
- Do not create Vue, SCSS, router, or topic files for LeetCode skeletons.
- Keep the file self-contained and runnable with the existing debug config.

## TypeScript Style

- Prefer explicit aliases from the LeetCode TypeScript signature.
- Keep placeholder implementation exactly like the LeetCode TypeScript starter when possible:

```ts
function fnName(args: Args): ReturnType {}
```

- For class-based tasks, preserve the class skeleton from LeetCode:

```ts
class TimeLimitedCache {
  constructor() {}

  set(key: number, value: number, duration: number): boolean {}

  get(key: number): number {}

  count(): number {}
}
```

- Do not add fake return values only to satisfy local TypeScript if LeetCode's starter leaves the body empty.
- Do not add clever helper abstractions in the skeleton.

## When Preparing From A Link

1. Open the LeetCode page or use the task data from the user if provided.
2. Switch the task language to TypeScript.
3. Extract:
   - problem number
   - title
   - difficulty
   - canonical URL
   - TypeScript signature
   - examples
   - constraints if useful
4. Create the file with the shape above.
5. Validate TypeScript syntax when possible.
6. Tell the user the created path.
