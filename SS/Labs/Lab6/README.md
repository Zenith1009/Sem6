# System Software Lab 6: Recursive Descent Parser

## Table of Contents
- [1. Problem Statement](#1-problem-statement)
- [2. Grammar](#2-grammar)
- [3. Program Structure (Code Explanation)](#3-program-structure-code-explanation)
- [4. Parsing Logic](#4-parsing-logic)
- [5. Input and Output Behavior](#5-input-and-output-behavior)
- [6. Compile and Run](#6-compile-and-run)
- [7. Sample Runs](#7-sample-runs)
- [8. Viva Quick Answers](#8-viva-quick-answers)

## 1. Problem Statement
Write a C program to implement recursive descent parsing for the given expression grammar and check whether an input string is accepted.

## 2. Grammar

```text
E  -> T E'
E' -> + T E' | @
T  -> F T'
T' -> * F T' | @
F  -> id | (E)
```

Here `@` means epsilon (empty production).

Given test strings:
- `a/c+d`
- `(a+b)*c`

## 3. Program Structure (Code Explanation)
Source file: [SS/Lab6/rdp_lab6.c](SS/Lab6/rdp_lab6.c)

### 3.1 Global State
- `input[200]`: stores the input expression.
- `pos`: current parsing index in `input`.
- `error`: set to `1` when parsing fails.

### 3.2 Function Mapping to Grammar
- `E()` implements `E -> T E'`
- `Eprime()` implements `E' -> + T E' | @`
- `T()` implements `T -> F T'`
- `Tprime()` implements `T' -> * F T' | @`
- `F()` implements `F -> id | (E)`

### 3.3 Helper Function
- `skip_space()` advances `pos` over spaces/tabs so parser can handle inputs with whitespace.

### 3.4 How `F()` Works in Code
`F()` accepts either:
- parenthesized expression: `(` `E` `)`
- identifier token: starts with alphabet and may continue with letters/digits (`isalnum` loop)

So the implementation accepts identifiers like `a`, `x1`, `temp2` (not only literal text `id`).

## 4. Parsing Logic
1. `main()` reads input and removes trailing newline.
2. Parsing starts with `E()`.
3. Each function checks grammar rule and recursively calls the next non-terminal function.
4. On mismatch, `error = 1`.
5. Final acceptance condition:
	- `error == 0`
	- all input consumed (`input[pos] == '\0'`) after skipping spaces.

This is top-down, predictive parsing without backtracking.

## 5. Input and Output Behavior
Input supports:
- identifiers (`a`, `abc`, `x12`)
- operators `+`, `*`
- parentheses `(` `)`
- optional spaces/tabs

Output:
- `Accepted` when string follows grammar.
- `Rejected` otherwise.

## 6. Compile and Run
```bash
gcc rdp_lab6.c -o rdp6
./rdp6
```

## 7. Sample Runs

### Case A
Input:
```text
a/c+d
```
Output:
```text
Rejected
```
Reason: `/` is not part of grammar (`*` is valid, `/` is not).

### Case B
Input:
```text
(a+b)*c
```
Output:
```text
Accepted
```

## 8. Viva Quick Answers
1. This is a recursive descent (top-down) parser.
2. No backtracking is used for this grammar.
3. `@` denotes epsilon production.
4. `*` has higher precedence than `+` because of grammar structure (`T` inside `E`).
5. Acceptance requires successful parse and full input consumption.
