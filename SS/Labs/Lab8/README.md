# System Software Lab 8: LL(1) Parsing Table Construction

## Table of Contents
- [1. Problem Statement](#1-problem-statement)
- [2. LL(1) Grammar Definition](#2-ll1-grammar-definition)
- [3. Given Grammar](#3-given-grammar)
- [4. FIRST and FOLLOW Sets](#4-first-and-follow-sets)
- [5. LL(1) Parsing Table](#5-ll1-parsing-table)
- [6. C Program](#6-c-program)
- [7. Compile and Run](#7-compile-and-run)
- [8. Expected Result](#8-expected-result)

## 1. Problem Statement
Define LL(1) grammar and write a program to construct LL(1) parsing table for:

```text
S -> aBDh
B -> cC
C -> bC | e
D -> EF
E -> g | e
F -> f | e
```

In code, epsilon is represented as `#`.

## 2. LL(1) Grammar Definition
A grammar is LL(1) if a top-down predictive parser can select exactly one production using only:
- Left-to-right input scan (`L`)
- Leftmost derivation (`L`)
- One-symbol lookahead (`1`)

There should be no parsing table conflicts (no multiple productions in one cell).

## 3. Given Grammar

```text
S -> aBDh
B -> cC
C -> bC | #
D -> EF
E -> g | #
F -> f | #
```

## 4. FIRST and FOLLOW Sets
The program computes FIRST and FOLLOW automatically.

Expected sets:

```text
FIRST(S) = { a }
FIRST(B) = { c }
FIRST(C) = { b, # }
FIRST(D) = { g, f, # }
FIRST(E) = { g, # }
FIRST(F) = { f, # }

FOLLOW(S) = { $ }
FOLLOW(B) = { g, f, h }
FOLLOW(C) = { g, f, h }
FOLLOW(D) = { h }
FOLLOW(E) = { f, h }
FOLLOW(F) = { h }
```

## 5. LL(1) Parsing Table
Main non-empty entries:

```text
M[S, a] = S -> aBDh
M[B, c] = B -> cC
M[C, b] = C -> bC
M[C, g] = C -> #
M[C, f] = C -> #
M[C, h] = C -> #
M[D, g] = D -> EF
M[D, f] = D -> EF
M[D, h] = D -> EF
M[E, g] = E -> g
M[E, f] = E -> #
M[E, h] = E -> #
M[F, f] = F -> f
M[F, h] = F -> #
```

No conflicts occur, so grammar is LL(1).

## 6. C Program
Source file: `SS/Labs/Lab8/ll1_lab8.c`

Program features:
- Stores grammar productions.
- Computes FIRST sets iteratively.
- Computes FOLLOW sets iteratively.
- Builds LL(1) table using FIRST/FOLLOW rules.
- Prints grammar status (LL(1) or not LL(1)).

## 7. Compile and Run

```bash
cd SS/Labs/Lab8
gcc ll1_lab8.c -o ll1
./ll1
```

## 8. Expected Result
The program prints FIRST, FOLLOW, and LL(1) parsing table and concludes:

```text
Grammar is LL(1).
```
