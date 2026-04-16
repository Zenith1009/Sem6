# System Software Lab 10: CLR(1) and LALR(1) Parse Table Construction

## Table of Contents
1. [Part 1 — CLR(1)](#part-1--clr1)
2. [Part 2 — LALR(1)](#part-2--lalr1)
3. [Key Differences: CLR(1) vs LALR(1)](#key-differences-clr1-vs-lalr1)
4. [Run](#run)

---

## Part 1 — CLR(1)

### Grammar
```
S → (S) | a
```

### Augmented Grammar
```
0: S' → S
1: S  → ( S )
2: S  → a
```

### Definition
CLR(1) (**C**anonical **LR(1)**) uses LR(1) items of the form `[A → α•β, a]` where `a` is a single terminal lookahead. The lookahead is computed precisely using FIRST sets, making CLR(1) more powerful than SLR(1).

### FIRST Sets
```
FIRST(S) = { (, a }
```

### LR(1) Item Sets

| State | Items |
|---|---|
| I0 | S'→•S,$  S→•(S),$  S→•a,$ |
| I1 | S'→S•,$ |
| I2 | S→a•,$ |
| I3 | S→(•S),$  S→•(S),)  S→•a,) |
| I4 | S→(S•),$ |
| I5 | S→a•,) |
| I6 | S→(•S),)  S→•(S),)  S→•a,) |
| I7 | S→(S)•,$ |
| I8 | S→(S•),) |
| I9 | S→(S)•,) |

### CLR(1) Parsing Table

| St | ( | ) | a | $ | S |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | s3 | - | s2 | - | 1 |
| 1 | - | - | - | acc | - |
| 2 | - | - | - | r2 | - |
| 3 | s6 | - | s5 | - | 4 |
| 4 | - | s7 | - | - | - |
| 5 | - | r2 | - | - | - |
| 6 | s6 | - | s5 | - | 8 |
| 7 | - | - | - | r1 | - |
| 8 | - | s9 | - | - | - |
| 9 | - | r1 | - | - | - |

**10 states, no conflicts — Grammar is CLR(1).**

### Sample Parse: `(a)`
| Stack | Input | Action |
|---|---|---|
| [0] | (a)$ | Shift 3 |
| [0,3] | a)$ | Shift 5 |
| [0,3,5] | )$ | Reduce r2 (S→a) |
| [0,3,4] | )$ | Shift 7 |
| [0,3,4,7] | $ | Reduce r1 (S→(S)) |
| [0,1] | $ | **ACCEPT** |

---

## Part 2 — LALR(1)

### Grammar
```
S → AA
A → aA | b
```

### Augmented Grammar
```
0: S' → S
1: S  → AA
2: A  → aA
3: A  → b
```

### Definition
**LALR(1)** (**L**ook**A**head **LR(1)**) merges LR(1) states that share the same **LR(0) core** (same items, ignoring lookaheads). Fewer states than CLR(1), but occasionally introduces reduce-reduce conflicts. It is strictly more powerful than SLR(1).

| Parser | Power | States for this grammar |
|---|---|---|
| SLR(1) | Weakest | 7 |
| LALR(1) | Middle | 7 (same — no merge conflicts) |
| CLR(1) | Strongest | More (separate lookahead states) |

### FIRST Sets
```
FIRST(S) = { a, b }
FIRST(A) = { a, b }
```

### LR(1) → LALR(1) State Merging

LR(1) builds states with distinct lookaheads. LALR(1) merges states with the same core:

| LR(1) States Merged | Core | Merged Lookaheads |
|---|---|---|
| I3 + I6 | A→a•A, A→•aA, A→•b | {a,b} ∪ {\$} = {a,b,\$} |
| I4 + I7 | A→b• | {a,b} ∪ {\$} = {a,b,\$} |
| I8 + I9 | A→aA• | {a,b} ∪ {\$} = {a,b,\$} |

Result: **7 LALR(1) states** (from LR(1) states), no conflicts.

### LALR(1) Parsing Table

| St | a | b | $ | S | A |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | s3 | s1 | - | 4 | 2 |
| 1 | r3 | r3 | r3 | - | - |
| 2 | s3 | s1 | - | - | 5 |
| 3 | s3 | s1 | - | - | 6 |
| 4 | - | - | acc | - | - |
| 5 | - | - | r1 | - | - |
| 6 | r2 | r2 | r2 | - | - |

### Parser Moves for `aaabb`

| Stack | Input | Action |
|---|---|---|
| [0] | aaabb$ | Shift 3 |
| [0,3] | aabb$ | Shift 3 |
| [0,3,3] | abb$ | Shift 3 |
| [0,3,3,3] | bb$ | Shift 1 |
| [0,3,3,3,1] | b$ | Reduce r3 (A→b) |
| [0,3,3,3,6] | b$ | Reduce r2 (A→aA) |
| [0,3,3,6] | b$ | Reduce r2 (A→aA) |
| [0,3,6] | b$ | Reduce r2 (A→aA) |
| [0,2] | b$ | Shift 1 |
| [0,2,1] | $ | Reduce r3 (A→b) |
| [0,2,5] | $ | Reduce r1 (S→AA) |
| [0,4] | $ | **ACCEPT** |

---

## Key Differences: CLR(1) vs LALR(1)

| Property | CLR(1) | LALR(1) |
|---|---|---|
| Items | LR(1): [A→α•β, a] | LR(1) merged by core |
| Lookahead source | FIRST-based, per-state | Merged from multiple LR(1) states |
| Number of states | More (no merging) | Fewer (merging reduces states) |
| Power | Strongest LR | Between SLR and CLR |
| Possible conflicts | None beyond LR(1) | May introduce R-R conflicts on merge |

---

## Run

```bash
cd SS/Labs/Lab10

# Part 1: CLR(1)
python3 clr1_lab10.py
# Enter: (a)  or  ((a))  or  a

# Part 2: LALR(1)
python3 lalr1_lab10.py
# Automatically shows moves for "aaabb"
# Then prompts for custom input (e.g. ab, aab, aaabb)
```
