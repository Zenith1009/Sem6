# System Software Lab 5: LL(1) Parser

## Table of Contents
- [1. Problem Statement](#1-problem-statement)
- [2. Grammar and Symbol Mapping](#2-grammar-and-symbol-mapping)
- [3. Program Structure (Code Explanation)](#3-program-structure-code-explanation)
- [4. Parsing Logic](#4-parsing-logic)
- [5. LL(1) Parse Table](#5-ll1-parse-table)
- [6. Input and Output Behavior](#6-input-and-output-behavior)
- [7. Compile and Run](#7-compile-and-run)
- [8. Sample Runs](#8-sample-runs)
- [9. Viva Quick Answers](#9-viva-quick-answers)
- [10. Language Accepted](#10-language-accepted)

## 1. Problem Statement
Write a C program to:
1. Construct an LL(1) parse table for the given expression grammar.
2. Parse a user input string using predictive parsing.
3. Print whether the string is `Accepted` or `Rejected`.

## 2. Grammar and Symbol Mapping
Grammar:

```text
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> id | (E)
```

Code mapping used in parser:
- `A` represents `E'`
- `B` represents `T'`
- `i` represents token `id`

So productions in code are:

```text
E -> TA
A -> +TA | e
T -> FB
B -> *FB | e
F -> i | (E)
```

## 3. Program Structure (Code Explanation)
Source file: [SS/Lab5/ll1_parser.c](SS/Lab5/ll1_parser.c)

### 3.1 Core Data Structures
- `Prod { lhs, rhs }`: stores one grammar production.
- `nt[]`, `t[]`: arrays of non-terminals and terminals.
- `p[]`: list of grammar productions.
- `first[][]`, `follow[][]`: FIRST and FOLLOW sets as character arrays.
- `table[][][]`: LL(1) parse table storing RHS strings.

### 3.2 Utility Functions
- `has(set, c)`: checks whether symbol `c` exists in set.
- `add(set, c)`: inserts symbol uniquely.
- `merge(dst, src, skip)`: copies symbols from one set to another (optionally skipping `e`).
- `idx(arr, n, c)`: generic symbol lookup used by `nt_idx` and `t_idx`.
- `is_terminal(c)`: checks whether symbol belongs to terminal list.

### 3.3 FIRST/FOLLOW Construction Functions
- `first_of_str(s, out)`: computes FIRST of a RHS/suffix string.
- `compute_first()`: iterative fixed-point computation of FIRST for all non-terminals.
- `compute_follow()`: iterative fixed-point computation of FOLLOW sets.

### 3.4 Parse Table and Parsing Functions
- `build_table()`: fills LL(1) table using FIRST and FOLLOW (table entries are not hardcoded).
- `normalize(raw, out)`: converts input token `id` to `i`, removes spaces, appends `$`.
- `parse(input)`: stack-based predictive parser using parse table.
- `print_table()`: prints LL(1) table in matrix format.
- `main()`: orchestration (compute sets, build table, read input, parse, print result).

## 4. Parsing Logic
High-level flow:
1. Compute `FIRST` and `FOLLOW`.
2. Build LL(1) table:
	- For `A -> α`, put `A -> α` in `M[A, a]` for each `a` in `FIRST(α) \ {e}`.
	- If `e ∈ FIRST(α)`, put `A -> e` in `M[A, b]` for each `b` in `FOLLOW(A)`.
3. Normalize input (`id` → `i`, append `$`).
4. Predictive parse using stack:
	- Start stack with `$E`.
	- Match terminals directly.
	- For non-terminal on top, consult table using current lookahead.
	- Accept only if both stack and input end at `$`.

## 5. LL(1) Parse Table

|     | i   | +    | *    | (   | )   | $   |
|-----|-----|------|------|-----|-----|-----|
| E   | TA  | -    | -    | TA  | -   | -   |
| A   | -   | +TA  | -    | -   | e   | e   |
| T   | FB  | -    | -    | FB  | -   | -   |
| B   | -   | e    | *FB  | -   | e   | e   |
| F   | i   | -    | -    | (E) | -   | -   |

## 6. Input and Output Behavior
Input tokens supported:
- `id`, `+`, `*`, `(`, `)`

Normalization rules:
- Spaces/tabs are ignored.
- `id` is converted to internal symbol `i`.
- `$` is appended as end marker.

Output:
- `Accepted` if input belongs to grammar.
- `Rejected` otherwise.

## 7. Compile and Run
```bash
gcc ll1_parser.c -o ll1
./ll1
```

## 8. Sample Runs
### Case 1
Input:
```text
id+id*id
```
Output:
```text
Accepted
```

### Case 2
Input:
```text
(id+id)*id
```
Output:
```text
Accepted
```

### Case 3
Input:
```text
id+*id
```
Output:
```text
Rejected
```

## 9. Viva Quick Answers
### 1) What type of grammar is this?
- Expression grammar transformed to LL(1) form using helper non-terminals `E'` and `T'`.

### 2) Why is it LL(1)?
- One lookahead symbol is enough to choose production.
- Parse table has no conflicts.

### 3) Why are FIRST and FOLLOW needed?
- FIRST fills normal parse-table entries.
- FOLLOW handles epsilon (`e`) productions.

### 4) FIRST sets
- `FIRST(E) = {(, id}`
- `FIRST(E') = {+, ε}`
- `FIRST(T) = {(, id}`
- `FIRST(T') = {*, ε}`
- `FIRST(F) = {(, id}`

### 5) FOLLOW sets
- `FOLLOW(E) = {), $}`
- `FOLLOW(E') = {), $}`
- `FOLLOW(T) = {+, ), $}`
- `FOLLOW(T') = {+, ), $}`
- `FOLLOW(F) = {*, +, ), $}`

### 6) Why stack-based parsing?
- LL(1) predictive parser is a non-recursive top-down parser.
- Stack stores expected symbols while input is scanned left-to-right.

### 7) Time complexity
- Parsing phase is `O(n)` for input length `n`.

### 8) Why use `A` and `B`?
- Single-character encoding simplifies table indexing in C arrays.

### 9) Immediate invalid cases
- Unknown token (not among `id + * ( )`).
- Operator misuse like `id+*id`.
- Unbalanced or missing parentheses.

### 10) Precedence and associativity
- `*` has higher precedence than `+` due to grammar layering (`T` inside `E`).
- Expressions behave left-associatively in parsing outcomes.

## 10. Language Accepted
The grammar accepts valid infix arithmetic expressions over:
- token `id`
- operators `+`, `*`
- balanced parentheses

Equivalent grammar-style pattern:

```text
expr  := term ( + term )*
term  := factor ( * factor )*
factor:= id | ( expr )
```

Note:
- Language is recursive (nested parentheses), so a single regular expression cannot represent it exactly.
