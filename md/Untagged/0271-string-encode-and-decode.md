# 271. Encode and Decode Strings (Medium) (<https://neetcode.io/problems/string-encode-and-decode/question?list=neetcode150>)

> Design an algorithm to encode a list of strings to a single string.
> The encoded string is then decoded back to the original list of strings.
> Constraints / Notes: - The input strings may contain any characters.
> - You must ensure the encoding is reversible without ambiguity.

```ts
class Codec {
  constructor() {

  }

  encode(strs: string[]): string {

  }

  decode(s: string): string[] {

  }
}


// Local check:
const codec = new Codec()

console.log(codec.decode(codec.encode(["hello", "world"])))
console.log(codec.decode(codec.encode(["lint", "code", "love", "you"])))
console.log(codec.decode(codec.encode([""])))
```

```md
Example 1:

    Input: ["hello","world"]
    Output: ["hello","world"]
    Explanation:
      After encoding and then decoding, we get the original array back.

  Example 2:

    Input: ["lint","code","love","you"]
    Output: ["lint","code","love","you"]
```
