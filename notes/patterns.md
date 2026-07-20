# Паттерны

Конспект для повторения перед собеседованием (30–60 минут). Один паттерн = один раздел: идея, шаблон кода, канонические задачи из этого репозитория и извне.

Ведётся по методике `leetcode-practice` скилла — пополняется после каждой сессии, где паттерн разбирался осознанно (не просто "решил задачу", а понял общий шаблон).

## Two Pointers

**Идея:** два индекса двигаются по структуре навстречу друг другу или в одном направлении, чтобы избежать вложенного перебора.

**Шаблон:**
```ts
let left = 0
let right = arr.length - 1
while (left < right) {
  // проверка/решение с arr[left], arr[right]
  // сдвиг left++ и/или right--
}
```

**Задачи в репо:**
- `solutions/Array/0011-container-with-most-water.ts`
- `solutions/Array/0015-3sum.ts`
- `solutions/Two Pointers/125-valid-palindrome.ts`
- `solutions/Two Pointers/151-reverse-words-in-a-string.ts`
- `solutions/Two Pointers/1768-merge-strings-alternately.ts`
- `solutions/Two Pointers/345-reverse-vowels-of-a-string.ts`
- `solutions/Two Pointers/392-is-subsequence.ts`
- `solutions/Two Pointers/844-backspace-string-compare.ts`

## Sliding Window

**Идея:** окно `[left, right]` расширяется/сужается по массиву/строке, инкрементально пересчитывая состояние вместо полного пересчёта на каждом шаге.

**Шаблон:**
```ts
let left = 0
let state = 0 // сумма/счётчик/множество в окне
for (let right = 0; right < arr.length; right++) {
  // добавить arr[right] в state
  while (/* окно невалидно */) {
    // убрать arr[left] из state
    left++
  }
  // обновить ответ по текущему окну
}
```

**Задачи в репо:**
- `solutions/Array/643-maximum-average-subarray-i.ts`

## Monotonic Stack

**Идея:** стек хранит индексы/значения в монотонном порядке; элемент выталкивается, когда находится "следующий больший/меньший" для него — амортизированный O(n) вместо O(n²).

**Шаблон:**
```ts
const stack: number[] = [] // индексы
const answer = new Array(arr.length).fill(0)
for (let i = 0; i < arr.length; i++) {
  while (stack.length && arr[i] > arr[stack.at(-1)!]) {
    const idx = stack.pop()!
    answer[idx] = i - idx
  }
  stack.push(i)
}
```

**Задачи в репо:**
- `solutions/Array/739-daily-temperatures.ts`
- `solutions/Stack/155-min-stack.ts`
- `solutions/String/20-valid-parentheses.ts`
- `solutions/Array/1441-build-an-array-with-stack-operations.ts`
- `solutions/Array/853-car-fleet.ts` — тот же инвариант без явного стека: идём от машины, ближней к target, к дальней, и держим одно число — время прибытия текущего лидирующего автопарка; если currentTime новой машины больше него — это новый автопарк.

## Hash Map / Frequency Counting

**Идея:** обменять O(n) память на O(1) проверку "видели ли мы это", "сколько раз", "есть ли пара до нужной суммы".

**Задачи в репо:**
- `solutions/Array/0049-group-anagrams.ts`
- `solutions/Array/128-longest-consecutive-sequence.ts`
- `solutions/Array/217-contains-duplicate.ts`
- `solutions/Array/347-top-k-frequent-elements.ts`
- `solutions/Hash Table/242-valid-anagram.ts`

## Binary Search

**Идея:** пространство ответов монотонно — можно делить пополам вместо линейного перебора.

**Шаблон:**
```ts
let lo = 0
let hi = arr.length - 1
while (lo <= hi) {
  const mid = lo + Math.floor((hi - lo) / 2)
  if (/* условие достигнуто */) return mid
  else if (/* нужно правее */) lo = mid + 1
  else hi = mid - 1
}
```

**Задачи в репо:** пока нет — следующая цель.

## Dynamic Programming

**Идея:** разбить задачу на перекрывающиеся подзадачи, кэшировать результат по инварианту (индекс, остаток, битовая маска и т.п.).

**Задачи в репо:** пока нет — следующая цель.

## Union-Find (DSU)

**Идея:** отслеживание компонент связности с почти-O(1) union/find через path compression + union by rank.

**Задачи в репо:** пока нет.

## Graph BFS/DFS, Dijkstra

**Идея:** BFS — кратчайший путь в невзвешенном графе; Dijkstra — кратчайший путь во взвешенном графе с неотрицательными весами (приоритетная очередь).

**Задачи в репо:** пока нет.

---

## Как пополнять

1. После сессии по `leetcode-practice`, если разобран новый паттерн — добавь раздел или дополни существующий: идея в 1-2 предложения, минимальный шаблон кода, ссылка на решённую задачу.
2. Не копируй решение задачи целиком — только обобщённый шаблон паттерна.
3. Держи "Задачи в репо" актуальным: путь должен существовать в `solutions/`.
