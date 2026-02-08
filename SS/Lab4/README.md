# System Software Lab 4

---

## Question 1: FIRST and FOLLOW Sets

`1. Write a C Program to find set of FIRST() and FOLLOW() for the given grammar`

### Problem Statement

Write a C Program to compute FIRST and FOLLOW sets for the following grammars:

**Grammar A:**
```
S → aSbS | bSaS | ∈
```

**Grammar B:**
```
E  → TE'
E' → +TE' | ε
T  → FT'
T' → *FT' | ε
F  → (E) | id
```

### Concept Understanding

**What is Syntax Analysis?**

Syntax analysis (parsing) is the second phase of compilation that verifies whether the sequence of tokens follows the grammatical rules of the language. To do this efficiently, compilers need to know:

1. **What can start a production?** → FIRST set
2. **What can come after a non-terminal?** → FOLLOW set

These sets are fundamental for building parsers, especially **LL(1) predictive parsers**.

**What are FIRST Sets?**

FIRST(α) is the set of terminals that can appear as the **first symbol** of any string derived from α.

**Definition:**
```
FIRST(α) = {a | α ⇒* aβ, where a is a terminal}
```

If α can derive ε (empty string), then ε ∈ FIRST(α).

**Examples:**

```
Grammar: E → TE'
         T → FT'
         F → (E) | id

FIRST(E) = FIRST(T) = FIRST(F) = {(, id}
  Why? E derives T, T derives F, F starts with ( or id

Grammar: E' → +TE' | ε
FIRST(E') = {+, ε}
  Why? E' can start with + or can derive nothing (ε)
```

**What are FOLLOW Sets?**

FOLLOW(A) is the set of terminals that can appear **immediately after** non-terminal A in some derivation.

**Definition:**
```
FOLLOW(A) = {a | S ⇒* αAaβ, where a is a terminal}
```

$ (end of input) is in FOLLOW of the start symbol.

**Examples:**

```
Grammar: E → TE'
         E' → +TE'

If we have production with E:
  F → (E)
  Then ) is in FOLLOW(E) because E is followed by )

Start symbol has $ in its FOLLOW:
  FOLLOW(E) = {$, )}
```

**Why Do We Need FIRST and FOLLOW?**

These sets are used to construct **parsing tables** for LL(1) parsers:

```
For production A → α:
  - If a ∈ FIRST(α), add A → α to table[A, a]
  - If ε ∈ FIRST(α), add A → α to table[A, b] for all b ∈ FOLLOW(A)
```

This allows the parser to decide which production to use by looking at just **one token ahead** (hence LL(1) - **1** lookahead).

**Algorithm to Compute FIRST Set**

```
FIRST(X) for non-terminal X:

1. If X → aα (a is terminal)
   Add a to FIRST(X)

2. If X → ε
   Add ε to FIRST(X)

3. If X → Y₁Y₂...Yₖ (all Yᵢ are non-terminals/terminals)
   - Add FIRST(Y₁) - {ε} to FIRST(X)
   - If ε ∈ FIRST(Y₁):
     - Add FIRST(Y₂) - {ε} to FIRST(X)
     - If ε ∈ FIRST(Y₂):
       - Add FIRST(Y₃) - {ε} to FIRST(X)
       - Continue...
   - If ε ∈ FIRST(all Yᵢ):
     - Add ε to FIRST(X)

For terminal: FIRST(a) = {a}
```

**Algorithm to Compute FOLLOW Set**

```
FOLLOW(A) for non-terminal A:

1. If A is start symbol:
   Add $ to FOLLOW(A)

2. For production B → αAβ:
   - Add FIRST(β) - {ε} to FOLLOW(A)
   - If ε ∈ FIRST(β) or β is empty:
     - Add FOLLOW(B) to FOLLOW(A)

Repeat until no new symbols are added.
```

**Step-by-Step Example: Grammar A**

```
Grammar: S → aSbS | bSaS | ε
```

**Computing FIRST(S):**

1. Production: S → aSbS
   - First symbol is 'a' (terminal)
   - Add 'a' to FIRST(S)

2. Production: S → bSaS
   - First symbol is 'b' (terminal)
   - Add 'b' to FIRST(S)

3. Production: S → ε
   - Add ε to FIRST(S)

**Result:** FIRST(S) = {a, b, ε}

**Computing FOLLOW(S):**

1. S is start symbol
   - Add $ to FOLLOW(S)

2. Production: S → aSbS
   - After first S: we have 'b'
   - Add 'b' to FOLLOW(S)
   - After second S: nothing (end of production)
   - Add FOLLOW(S) to FOLLOW(S) (already have $)

3. Production: S → bSaS
   - After first S: we have 'a'
   - Add 'a' to FOLLOW(S)
   - After second S: nothing
   - Add FOLLOW(S) to FOLLOW(S)

**Result:** FOLLOW(S) = {$, a, b}

**Step-by-Step Example: Grammar B**

```
E  → TE'
E' → +TE' | ε
T  → FT'
T' → *FT' | ε
F  → (E) | id
```

**Computing FIRST sets:**

```
FIRST(F):
  - F → (E): starts with '(' → add '('
  - F → id: starts with 'id' → add 'id'
  Result: FIRST(F) = {(, id}

FIRST(T'):
  - T' → *FT': starts with '*' → add '*'
  - T' → ε: → add ε
  Result: FIRST(T') = {*, ε}

FIRST(T):
  - T → FT': starts with F
  - Add FIRST(F) - {ε} = {(, id}
  Result: FIRST(T) = {(, id}

FIRST(E'):
  - E' → +TE': starts with '+' → add '+'
  - E' → ε: → add ε
  Result: FIRST(E') = {+, ε}

FIRST(E):
  - E → TE': starts with T
  - Add FIRST(T) - {ε} = {(, id}
  Result: FIRST(E) = {(, id}
```

**Computing FOLLOW sets:**

```
FOLLOW(E):
  - E is start symbol → add $
  - F → (E): E followed by ')' → add ')'
  Result: FOLLOW(E) = {$, )}

FOLLOW(E'):
  - E → TE': E' at end → add FOLLOW(E) = {$, )}
  - E' → +TE': E' at end → add FOLLOW(E') (recursive)
  Result: FOLLOW(E') = {$, )}

FOLLOW(T):
  - E → TE': T followed by E'
  - E' can derive ε, so add FIRST(E') - {ε} = {+}
  - E' can derive ε, so add FOLLOW(E) = {$, )}
  - E' → +TE': T followed by E', same logic
  Result: FOLLOW(T) = {+, $, )}

FOLLOW(T'):
  - T → FT': T' at end → add FOLLOW(T) = {+, $, )}
  - T' → *FT': T' at end → add FOLLOW(T') (recursive)
  Result: FOLLOW(T') = {+, $, )}

FOLLOW(F):
  - T → FT': F followed by T'
  - T' can derive ε, so add FIRST(T') - {ε} = {*}
  - T' can derive ε, so add FOLLOW(T) = {+, $, )}
  - T' → *FT': F followed by T', same logic
  Result: FOLLOW(F) = {*, +, $, )}
```

### Code Understanding

**Grammar A (grammar_a.c):**

For Grammar A, the sets are calculated manually since the grammar is simple:

```c
// FIRST(S) = {a, b, ε}
add_first('a');  // from S -> aSbS
add_first('b');  // from S -> bSaS
add_first('e');  // from S -> ε

// FOLLOW(S) = {$, a, b}
add_follow('$');  // S is start symbol
add_follow('a');  // from S -> bSaS (a comes after S)
add_follow('b');  // from S -> aSbS (b comes after S)
```

**Grammar B (grammar_b.c):**

For Grammar B, we calculate sets by following the rules:

```c
void compute_first() {
    // Start from innermost non-terminals
    // F -> (E) | id, so FIRST(F) = {(, id}
    // T' -> *FT' | ε, so FIRST(T') = {*, ε}
    // T -> FT', so FIRST(T) = FIRST(F) = {(, id}
    // E' -> +TE' | ε, so FIRST(E') = {+, ε}
    // E -> TE', so FIRST(E) = FIRST(T) = {(, id}
}

void compute_follow() {
    // FOLLOW(E): start symbol gets $, and ) from F -> (E)
    // FOLLOW(E'): same as FOLLOW(E) since E -> TE'
    // FOLLOW(T): + from FIRST(E'), and FOLLOW(E) since E' can be ε
    // FOLLOW(T'): same as FOLLOW(T) since T -> FT'
    // FOLLOW(F): * from FIRST(T'), and FOLLOW(T) since T' can be ε
}
```

### Expected Output

**Grammar A:**
```
FIRST(S) = { a, b, ε }
FOLLOW(S) = { $, a, b }
```

**Grammar B:**
```
FIRST(E)  = { (, id }
FIRST(E') = { +, ε }
FIRST(T)  = { (, id }
FIRST(T') = { *, ε }
FIRST(F)  = { (, id }

FOLLOW(E)  = { $, ) }
FOLLOW(E') = { $, ) }
FOLLOW(T)  = { +, $, ) }
FOLLOW(T') = { +, $, ) }
FOLLOW(F)  = { *, +, $, ) }
```

### Viva Prep

**Q: What is the FIRST set?**
A: FIRST(α) is the set of terminals that can appear as the first symbol of any string derived from α. If α can derive ε, then ε ∈ FIRST(α).

**Q: What is the FOLLOW set?**
A: FOLLOW(A) is the set of terminals that can appear immediately after non-terminal A in some derivation. $ (end-of-input) is in FOLLOW of start symbol.

**Q: Why do we need FIRST and FOLLOW sets?**
A: They are used to construct **parsing tables** for LL(1) predictive parsers. They help determine which production to use based on the current input token.

**Q: How do you compute FIRST of a production X → Y₁Y₂...Yₖ?**
A:
1. Add FIRST(Y₁) - {ε} to FIRST(X)
2. If ε ∈ FIRST(Y₁), add FIRST(Y₂) - {ε}, and so on
3. If all Yᵢ can derive ε, add ε to FIRST(X)

**Q: How do you compute FOLLOW of A in production B → αAβ?**
A:
1. Add FIRST(β) - {ε} to FOLLOW(A)
2. If β can derive ε or is empty, add FOLLOW(B) to FOLLOW(A)

**Q: When is ε included in FIRST set?**
A: When a non-terminal has a production that derives ε directly (X → ε) or derives ε through all symbols in RHS (X → Y₁Y₂ where all Yᵢ derive ε).

**Q: Is ε ever in FOLLOW set?**
A: No, FOLLOW sets contain only terminals and $ (end-marker). Epsilon is never in FOLLOW.

**Q: Why do we need multiple iterations for FOLLOW computation?**
A: Because FOLLOW sets have dependencies. For example, FOLLOW(A) might depend on FOLLOW(B), which might not be computed yet. Multiple passes resolve all dependencies.

**Q: What is the difference between nullable and epsilon?**
A: A non-terminal is **nullable** if it can derive ε. Epsilon (ε) itself represents the empty string. If X is nullable, then ε ∈ FIRST(X).

**Q: How are FIRST and FOLLOW used in parsing?**
A: For production A → α:
- If terminal a ∈ FIRST(α), use A → α when input is a
- If ε ∈ FIRST(α) and b ∈ FOLLOW(A), use A → α when input is b

**Q: What is LL(1) grammar?**
A: A grammar where we can determine which production to use by looking at exactly **1** token ahead. FIRST and FOLLOW sets must be disjoint for this.

**Q: What is the condition for LL(1)?**
A: For every production A → α | β:
1. FIRST(α) ∩ FIRST(β) = ∅
2. If ε ∈ FIRST(α), then FIRST(β) ∩ FOLLOW(A) = ∅

**Q: Can left-recursive grammars be LL(1)?**
A: No. Left recursion (A → Aα) violates LL(1) conditions. Must eliminate left recursion first.

**Q: What is the significance of $ in FOLLOW set?**
A: $ represents end-of-input. It's always in FOLLOW of the start symbol and helps determine when a production deriving ε should be used at end of input.

**Q: How do you handle epsilon productions?**
A: 
- In FIRST: Add ε if production is X → ε
- In FOLLOW: If A → αBβ and β derives ε, add FOLLOW(A) to FOLLOW(B)

**Q: What is the time complexity?**
A: 
- FIRST: O(n²) where n is grammar size
- FOLLOW: O(n³) due to multiple iterations and dependencies

---

## Quick Reference

### How to Compile and Run

```bash
# Grammar A
gcc grammar_a.c -o grammar_a
./grammar_a

# Grammar B
gcc grammar_b.c -o grammar_b
./grammar_b
```

### Output

**Grammar A:**
```
Grammar A:
S -> aSbS | bSaS | e

FIRST(S) = { a, b, ε }

FOLLOW(S) = { $, a, b }
```

**Grammar B:**
```
Grammar B:
E  -> T E'
E' -> +T E' | e
T  -> F T'
T' -> *F T' | e
F  -> (E) | id

FIRST SETS:
FIRST(E) = { (, id }
FIRST(E') = { +, ε }
FIRST(T) = { (, id }
FIRST(T') = { *, ε }
FIRST(F) = { (, id }

FOLLOW SETS:
FOLLOW(E) = { $, ) }
FOLLOW(E') = { $, ) }
FOLLOW(T) = { +, $, ) }
FOLLOW(T') = { +, $, ) }
FOLLOW(F) = { *, +, $, ) }
```

### Expected Results

**Grammar A:**

| Non-Terminal | FIRST | FOLLOW |
|--------------|-------|--------|
| S | {a, b, ε} | {$, a, b} |

**Grammar B:**

| Non-Terminal | FIRST | FOLLOW |
|--------------|-------|--------|
| E | {(, id} | {$, )} |
| E' | {+, ε} | {$, )} |
| T | {(, id} | {+, $, )} |
| T' | {*, ε} | {+, $, )} |
| F | {(, id} | {*, +, $, )} |

### Files in Lab4/

| File | Purpose |
|------|---------|
| `grammar_a.c` | FIRST and FOLLOW for Grammar A |
| `grammar_b.c` | FIRST and FOLLOW for Grammar B |
| `README.md` | This documentation file |

### Key Concepts Summary

| Concept | Description |
|---------|-------------|
| FIRST(α) | Terminals that can start strings derived from α |
| FOLLOW(A) | Terminals that can follow non-terminal A |
| Epsilon (ε) | Empty string, in FIRST but never in FOLLOW |
| $ (dollar) | End-of-input marker, in FOLLOW of start symbol |
| LL(1) | Left-to-right, Leftmost, 1 lookahead parsing |
| Predictive parsing | Using FIRST/FOLLOW to build parsing table |
| Nullable | Non-terminal that can derive ε |

### Algorithm Summary

**FIRST Computation:**
1. If X → a... (terminal), add a to FIRST(X)
2. If X → ε, add ε to FIRST(X)
3. If X → Y₁...Yₖ, add FIRST(Y₁) - {ε}
4. If Y₁ nullable, add FIRST(Y₂) - {ε}, etc.
5. If all nullable, add ε to FIRST(X)

**FOLLOW Computation:**
1. Add $ to FOLLOW(start symbol)
2. For A → αBβ: add FIRST(β) - {ε} to FOLLOW(B)
3. If β nullable or empty: add FOLLOW(A) to FOLLOW(B)
4. Repeat until no changes
Grammar B:
E  -> T E'
E' -> +T E' | e
T  -> F T'
T' -> *F T' | e
F  -> (E) | id

FIRST SETS:
FIRST(E) = { (, id }
FIRST(E') = { +, ε }
FIRST(T) = { (, id }
FIRST(T') = { *, ε }
FIRST(F) = { (, id }

FOLLOW SETS:
FOLLOW(E) = { $, ) }
FOLLOW(E') = { $, ) }
FOLLOW(T) = { +, $, ) }
FOLLOW(T') = { +, $, ) }
FOLLOW(F) = { *, +, $, )