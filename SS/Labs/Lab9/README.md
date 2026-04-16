# System Software Lab 9: SLR(1) Parse Table Construction

## Table of Contents
1. [Problem Statement](#1-problem-statement)
2. [SLR(1) Definition](#2-slr1-definition)
3. [Augmented Grammar](#3-augmented-grammar)
4. [FIRST and FOLLOW Sets](#4-first-and-follow-sets)
5. [LR(0) Item Sets](#5-lr0-item-sets)
6. [SLR(1) Parsing Table](#6-slr1-parsing-table)
7. [String Acceptance](#7-string-acceptance)
8. [C Program](#8-c-program)
9. [Compile and Run](#9-compile-and-run)
10. [Expected Output](#10-expected-output)

---

## 1. Problem Statement

Write a program to construct the SLR(1) parse table for the following grammar and check whether a given input string is accepted or not.

```
S → a B D h
B → c C
C → b C | ε
D → E F
E → g | ε
F → f | ε
```
*(ε = epsilon; represented as `#` in code)*

---

## 2. SLR(1) Definition

SLR(1) stands for **Simple LR with 1 lookahead**. It is a bottom-up parsing technique:

| Property | Description |
|---|---|
| **S** | Simple — uses FOLLOW sets to resolve reduce conflicts |
| **L** | Left-to-right scan of input |
| **R** | Rightmost derivation (in reverse) |
| **1** | One symbol of lookahead |

An SLR(1) parser uses:
- **LR(0) items** to build a canonical collection of states
- **Action table** — tells the parser to shift, reduce, or accept based on current state + lookahead terminal
- **Goto table** — tells the parser the next state after a reduction

A grammar is SLR(1) if the parse table has **no conflicts** (no cell with more than one action).

---

## 3. Augmented Grammar

An augmented start production `S' → S` is added to mark acceptance:

```
0:  S' → S
1:  S  → a B D h
2:  B  → c C
3:  C  → b C
4:  C  → #          (epsilon)
5:  D  → E F
6:  E  → g
7:  E  → #          (epsilon)
8:  F  → f
9:  F  → #          (epsilon)
```

---

## 4. FIRST and FOLLOW Sets

### FIRST Sets

| Non-terminal | FIRST |
|---|---|
| S | { a } |
| B | { c } |
| C | { b, ε } |
| D | { g, f, ε } |
| E | { g, ε } |
| F | { f, ε } |

### FOLLOW Sets

| Non-terminal | FOLLOW |
|---|---|
| S | { $ } |
| B | { g, f, h } |
| C | { g, f, h } |
| D | { h } |
| E | { f, h } |
| F | { h } |

---

## 5. LR(0) Item Sets

| State | Items |
|---|---|
| **I0** | S'→•S, S→•aBDh |
| **I1** | S'→S• |
| **I2** | S→a•BDh, B→•cC |
| **I3** | S→aB•Dh, D→•EF, E→•g, E→[•] |
| **I4** | B→c•C, C→•bC, C→[•] |
| **I5** | S→aBD•h |
| **I6** | D→E•F, F→•f, F→[•] |
| **I7** | E→g• |
| **I8** | B→cC• |
| **I9** | C→b•C, C→•bC, C→[•] |
| **I10** | S→aBDh• |
| **I11** | D→EF• |
| **I12** | F→f• |
| **I13** | C→bC• |

> **[•]** denotes a completed (reduce) item — `X→α•` where dot is at the end.

---

## 6. SLR(1) Parsing Table

### Action Table

| State | a | b | c | f | g | h | $ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | s2 | - | - | - | - | - | - |
| 1 | - | - | - | - | - | - | **acc** |
| 2 | - | - | s4 | - | - | - | - |
| 3 | - | - | - | r7 | s7 | r7 | - |
| 4 | - | s9 | - | r4 | r4 | r4 | - |
| 5 | - | - | - | - | - | s10 | - |
| 6 | - | - | - | s12 | - | r9 | - |
| 7 | - | - | - | r6 | - | r6 | - |
| 8 | - | - | - | r2 | r2 | r2 | - |
| 9 | - | s9 | - | r4 | r4 | r4 | - |
| 10 | - | - | - | - | - | - | r1 |
| 11 | - | - | - | - | - | r5 | - |
| 12 | - | - | - | - | - | r8 | - |
| 13 | - | - | - | r3 | r3 | r3 | - |

### Goto Table

| State | S | B | C | D | E | F |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 1 | - | - | - | - | - |
| 2 | - | 3 | - | - | - | - |
| 3 | - | - | - | 5 | 6 | - |
| 4 | - | - | 8 | - | - | - |
| 6 | - | - | - | - | - | 11 |
| 9 | - | - | 13 | - | - | - |

> **s**_n_ = shift to state _n_ &nbsp;|&nbsp; **r**_n_ = reduce by production _n_ &nbsp;|&nbsp; **-** = error &nbsp;|&nbsp; **acc** = accept

**No conflicts → Grammar is SLR(1).**

---

## 7. String Acceptance

### Parsing trace for `acbgfh`

| Stack | Input | Action | Detail |
|---|---|---|---|
| 0 | acbgfh$ | Shift | → 2 |
| 0,2 | cbgfh$ | Shift | → 4 |
| 0,2,4 | bgfh$ | Shift | → 9 |
| 0,2,4,9 | gfh$ | Reduce | r4: C→ε |
| 0,2,4,9,13 | gfh$ | Reduce | r3: C→bC |
| 0,2,4,8 | gfh$ | Reduce | r2: B→cC |
| 0,2,3 | gfh$ | Shift | → 7 |
| 0,2,3,7 | fh$ | Reduce | r6: E→g |
| 0,2,3,6 | fh$ | Shift | → 12 |
| 0,2,3,6,12 | h$ | Reduce | r8: F→f |
| 0,2,3,6,11 | h$ | Reduce | r5: D→EF |
| 0,2,3,5 | h$ | Shift | → 10 |
| 0,2,3,5,10 | $ | Reduce | r1: S→aBDh |
| 0,1 | $ | **ACCEPT** | |

### Summary of test strings

| Input | Result |
|---|---|
| `acbgfh` | ✅ ACCEPTED |
| `acgh` | ✅ ACCEPTED |
| `ach` | ✅ ACCEPTED |
| `acbh` | ✅ ACCEPTED |
| `acbfh` | ✅ ACCEPTED |
| `abch` | ❌ REJECTED |

---

## 8. C Program

File: `slr1_lab9.c`

### Program Features
- Stores the augmented grammar as an array of productions
- Computes FIRST sets iteratively (handles epsilon)
- Computes FOLLOW sets iteratively
- Builds LR(0) canonical item sets using closure and goto operations
- Constructs SLR(1) Action and Goto tables
- Detects shift-reduce / reduce-reduce conflicts
- Simulates stack-based parsing for any input string and reports ACCEPT/REJECT with full trace

---

## 9. Compile and Run

```bash
cd SS/Labs/Lab9
gcc slr1_lab9.c -o slr1
./slr1
```

To test a custom string, call `parse_string("your_input")` inside `main()`.

---

## 10. Expected Output

```
=== Lab 9: SLR(1) Parse Table Construction ===

FIRST(S) = { a }
FIRST(B) = { c }
FIRST(C) = { b, ε }
FIRST(D) = { f, g, ε }
FIRST(E) = { g, ε }
FIRST(F) = { f, ε }

FOLLOW(S) = { $ }
FOLLOW(B) = { f, g, h }
FOLLOW(C) = { f, g, h }
FOLLOW(D) = { h }
FOLLOW(E) = { f, h }
FOLLOW(F) = { h }

=== LR(0) Item Sets ===
I0: ... (14 states total)

=== SLR(1) Parsing Table ===
(14 states, no conflicts)

No conflicts — Grammar is SLR(1).

--- Parsing "acbgfh" ---  =>  ACCEPTED
--- Parsing "abch"   ---  =>  REJECTED
```
