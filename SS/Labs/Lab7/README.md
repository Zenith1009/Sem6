# System Software Lab 7: LR(0) and SLR Parse Table Construction

## Table of Contents
- [1. Problem Statement](#1-problem-statement)
- [2. Grammar](#2-grammar)
- [3. Augmented Grammar and Item Sets](#3-augmented-grammar-and-item-sets)
- [4. LR(0) Parse Table](#4-lr0-parse-table)
- [5. SLR Parse Table](#5-slr-parse-table)
- [6. Parser Moves for Given Inputs](#6-parser-moves-for-given-inputs)
- [7. C Program](#7-c-program)
- [8. Compile and Run](#8-compile-and-run)
- [9. Result Summary](#9-result-summary)

## 1. Problem Statement
Write a program to construct LR(0) and SLR parse tables for the grammar:

```text
E -> T T
T -> a T | b
```

Then check whether the given strings are accepted and show parser moves for:
- `aabb`
- `babb`

## 2. Grammar

```text
(1) E -> T T
(2) T -> a T
(3) T -> b
```

Augmented grammar:

```text
(0) S' -> E
```

## 3. Augmented Grammar and Item Sets

Canonical LR(0) item sets used:

```text
I0: S'->.E, E->.TT, T->.aT, T->.b
I1: S'->E.
I2: E->T.T, T->.aT, T->.b
I3: T->a.T, T->.aT, T->.b
I4: T->b.
I5: E->TT.
I6: T->aT.
```

Transitions:
- `I0 --E--> I1`
- `I0 --T--> I2`
- `I0 --a--> I3`
- `I0 --b--> I4`
- `I2 --T--> I5`
- `I2 --a--> I3`
- `I2 --b--> I4`
- `I3 --T--> I6`
- `I3 --a--> I3`
- `I3 --b--> I4`

## 4. LR(0) Parse Table

`ACTION` columns: `a, b, $` and `GOTO` columns: `E, T`

```text
State |   a   b   $  ||  E   T
--------------------------------
	0   | s3  s4  -   || 1   2
	1   | -   -   acc || -   -
	2   | s3  s4  -   || -   5
	3   | s3  s4  -   || -   6
	4   | r3  r3  r3  || -   -
	5   | r1  r1  r1  || -   -
	6   | r2  r2  r2  || -   -
```

Where:
- `r1: E -> T T`
- `r2: T -> a T`
- `r3: T -> b`

## 5. SLR Parse Table

FOLLOW sets:
- `FOLLOW(E) = { $ }`
- `FOLLOW(T) = { a, b, $ }`

SLR table:

```text
State |   a   b   $  ||  E   T
--------------------------------
	0   | s3  s4  -   || 1   2
	1   | -   -   acc || -   -
	2   | s3  s4  -   || -   5
	3   | s3  s4  -   || -   6
	4   | r3  r3  r3  || -   -
	5   | -   -   r1  || -   -
	6   | r2  r2  r2  || -   -
```

## 6. Parser Moves for Given Inputs

Below are SLR parser moves (the program also prints LR(0) moves).

### 6.1 Input: `aabb`

```text
Step | Stack                     | Input  | Action
------------------------------------------------------
1    | 0                         | aabb$  | shift 3
2    | 0 a 3                     | abb$   | shift 3
3    | 0 a 3 a 3                 | bb$    | shift 4
4    | 0 a 3 a 3 b 4             | b$     | reduce T -> b
5    | 0 a 3 a 3 T 6             | b$     | reduce T -> a T
6    | 0 a 3 T 6                 | b$     | reduce T -> a T
7    | 0 T 2                     | b$     | shift 4
8    | 0 T 2 b 4                 | $      | reduce T -> b
9    | 0 T 2 T 5                 | $      | reduce E -> T T
10   | 0 E 1                     | $      | accept
```

Result: `aabb` is accepted.

### 6.2 Input: `babb`

```text
Step | Stack                     | Input  | Action
------------------------------------------------------
1    | 0                         | babb$  | shift 4
2    | 0 b 4                     | abb$   | reduce T -> b
3    | 0 T 2                     | abb$   | shift 3
4    | 0 T 2 a 3                 | bb$    | shift 4
5    | 0 T 2 a 3 b 4             | b$     | reduce T -> b
6    | 0 T 2 a 3 T 6             | b$     | reduce T -> a T
7    | 0 T 2 T 5                 | b$     | error
```

Result: `babb` is rejected.

## 7. C Programs
Source files:
- `SS/Labs/Lab7/lr0_lab7.c` (LR(0) only)
- `SS/Labs/Lab7/slr_lab7.c` (SLR only)

What these programs do:
- Keep LR(0) and SLR logic in separate files.
- Print the corresponding parse table.
- Take one user input string over `{a,b}`.
- Show parser moves and final accepted/rejected result.

## 8. Compile and Run

```bash
cd SS/Labs/Lab7
gcc lr0_lab7.c -o lr0
./lr0

gcc slr_lab7.c -o slr
./slr
```

## 9. Result Summary
- Both LR(0) and SLR parsers accept `aabb`.
- Both LR(0) and SLR parsers reject `babb`.
- Hence the required input checking is successfully demonstrated with parser move traces.
