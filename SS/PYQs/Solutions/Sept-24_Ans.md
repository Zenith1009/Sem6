# System Software - Expected Answer Sheet

## September 2024 Mid Semester Paper

Course: CS301 - System Software  
Exam: Mid Semester Examination - September 2024  
Max Marks: 30

This answer sheet is written in student-answer style and sized according to the mark distribution. Where useful, compact derivation steps are shown so the final answer is easy to reproduce in an exam.

---

## Q1

### (a) Role of lexical analyser and why it is a separate phase [2 marks]

The lexical analyser is the first phase of the compiler. It reads the source program character by character and groups characters into meaningful units called tokens such as identifiers, keywords, operators, constants and delimiters.

Main roles:

1. Remove white spaces, newlines and comments.
2. Recognize tokens and pass them to the parser.
3. Create entries in the symbol table for identifiers/literals.
4. Detect lexical errors such as invalid identifiers or illegal characters.

It is kept as a separate phase because:

1. Token recognition is simpler and faster when isolated from syntax analysis.
2. The parser can work on tokens instead of raw characters.
3. Compiler design becomes modular, easier to implement, test and maintain.
4. Buffering and symbol-table handling can be optimized independently.

---

### (b) Techniques for look-ahead on input to identify tokens (input buffering schemes) [2 marks]

To identify tokens, the lexical analyser often needs look-ahead. For example, after seeing `<`, it must check whether the next character is `=` to decide between `<` and `<=`.

Common buffering schemes:

1. Single buffer scheme:
   Use one input buffer and two pointers, `lexemeBegin` and `forward`. This works, but checking end-of-buffer repeatedly is costly.

2. Sentinel scheme:
   Put a special sentinel character at the end of the buffer so each character read need not test separately for end-of-buffer.

3. Double buffer scheme:
   Use two half-buffers. When one half becomes empty, the other is refilled. Sentinels are placed at the ends. This is the standard efficient technique because it supports retract and multi-character look-ahead without frequent I/O checks.

Hence, the most practical scheme is two-buffer input buffering with sentinels.

---

## Q2

### (a) Eliminate left recursion and left factor the grammar [2 marks]

Given grammar:

```text
E -> aba | abba | Ea | EbE
```

Immediate left recursion exists because of:

```text
E -> Ea | EbE
```

Take:

```text
beta  = aba , abba
alpha = a , bE
```

After eliminating left recursion:

```text
E  -> aba E' | abba E'
E' -> a E' | bE E' | e
```

Now left factor `E`:

```text
E  -> ab X E'
X  -> a | ba
E' -> a E' | bE E' | e
```

Final answer:

```text
E  -> ab X E'
X  -> a | ba
E' -> a E' | bE E' | e
```

---

### (b) Show ambiguity and write an unambiguous grammar [3 marks]

Given grammar:

```text
E -> E + E | E * E | (E) | id
```

This grammar is ambiguous because the string:

```text
id + id * id
```

has two different parse trees:

1. `(id + id) * id`
2. `id + (id * id)`

So the grammar is ambiguous.

Now we need an unambiguous grammar such that:

1. `+` has higher precedence
2. `*` has lower precedence
3. both are left associative

To make `+` higher precedence than `*`, the `+` operator must be handled at the lower level.

Unambiguous grammar:

```text
E -> E * T | T
T -> T + F | F
F -> (E) | id
```

Why this works:

1. `T` handles `+`, so `+` binds more tightly.
2. `E` handles `*`, so `*` is lower precedence.
3. Left recursion in `E -> E * T` and `T -> T + F` gives left associativity.

---

### (c) Check whether the grammar is LL(2) using predictive parse table [3 marks]

Given grammar:

```text
X -> X S b | S a | b
S -> S b | X a | a
```

This grammar has immediate left recursion in both `X` and `S`, so it is already suspicious for predictive parsing.

For LL(2), we compute 2-symbol look-ahead sets.

Since both `X` and `S` can start with either `a` or `b`, the first two-symbol prefixes are:

```text
FIRST2(XSb) = {aa, ab, ba, bb}
FIRST2(Sa)  = {aa, ab, ba, bb}
FIRST2(b)   = {b$}

FIRST2(Sb)  = {aa, ab, ba, bb}
FIRST2(Xa)  = {aa, ab, ba, bb}
FIRST2(a)   = {a$}
```

So the predictive parse table for 2-symbol look-ahead has the following essential entries:

| Non-terminal | `aa` | `ab` | `ba` | `bb` | `a$` | `b$` |
|---|---|---|---|---|---|---|
| `X` | `X -> XSb` and `X -> Sa` | `X -> XSb` and `X -> Sa` | `X -> XSb` and `X -> Sa` | `X -> XSb` and `X -> Sa` | error | `X -> b` |
| `S` | `S -> Sb` and `S -> Xa` | `S -> Sb` and `S -> Xa` | `S -> Sb` and `S -> Xa` | `S -> Sb` and `S -> Xa` | `S -> a` | error |

Because multiple productions appear in the same cell, the table has conflicts.

Therefore:

```text
The grammar is NOT LL(2).
```

Steps for construction of LL(2) table:

1. Find the terminals that can begin each production.
2. Compute 2-symbol look-ahead sets `FIRST2` for each right-hand side.
3. Enter the production in all table cells corresponding to those 2-symbol prefixes.
4. If any cell gets more than one production, the grammar is not LL(2).

Here, conflicts occur for both `X` and `S`, hence not LL(2).

---

## Q3

### (a) Canonical LR(0) items, transition diagram, LR(0) table, parse `*id=id`, and justify LR(0) or not [3 marks]

Augmented grammar:

```text
S' -> S
S  -> L = R | R
L  -> *R | id
R  -> L
```

Number the productions:

```text
(1) S -> L = R
(2) S -> R
(3) L -> *R
(4) L -> id
(5) R -> L
```

#### Canonical collection of LR(0) items

```text
I0:
S' -> .S
S  -> .L=R
S  -> .R
L  -> .*R
L  -> .id
R  -> .L

I1:
L  -> * .R
R  -> .L
L  -> .*R
L  -> .id

I2:
S  -> L .= R
R  -> L .

I3:
S  -> R .

I4:
S' -> S .

I5:
L  -> id .

I6:
R  -> L .

I7:
L  -> *R .

I8:
S  -> L= .R
R  -> .L
L  -> .*R
L  -> .id

I9:
S  -> L=R .
```

#### Transition diagram

```text
I0 --*-->  I1
I0 --L-->  I2
I0 --R-->  I3
I0 --S-->  I4
I0 --id--> I5

I1 --*-->  I1
I1 --L-->  I6
I1 --R-->  I7
I1 --id--> I5

I2 --=-->  I8

I8 --*-->  I1
I8 --L-->  I6
I8 --R-->  I9
I8 --id--> I5
```

#### LR(0) parsing table

| State | `id` | `*` | `=` | `$` | `S` | `L` | `R` |
|---|---|---|---|---|---|---|---|
| 0 | `s5` | `s1` | - | - | 4 | 2 | 3 |
| 1 | `s5` | `s1` | - | - | - | 6 | 7 |
| 2 | `r5` | `r5` | `s8 / r5` | `r5` | - | - | - |
| 3 | `r2` | `r2` | `r2` | `r2` | - | - | - |
| 4 | - | - | - | `acc` | - | - | - |
| 5 | `r4` | `r4` | `r4` | `r4` | - | - | - |
| 6 | `r5` | `r5` | `r5` | `r5` | - | - | - |
| 7 | `r3` | `r3` | `r3` | `r3` | - | - | - |
| 8 | `s5` | `s1` | - | - | - | 6 | 9 |
| 9 | `r1` | `r1` | `r1` | `r1` | - | - | - |

State `2` has a shift/reduce conflict on `=`.

#### Parsing the input `*id = id`

If we choose shift on `=` at the conflict state, the string is accepted. A compact trace is:

| Step | Stack (states) | Input | Action |
|---|---|---|---|
| 1 | `0` | `* id = id $` | `s1` |
| 2 | `0 1` | `id = id $` | `s5` |
| 3 | `0 1 5` | `= id $` | `r4 : L -> id` |
| 4 | `0 1 6` | `= id $` | `r5 : R -> L` |
| 5 | `0 1 7` | `= id $` | `r3 : L -> *R` |
| 6 | `0 2` | `= id $` | `s8` |
| 7 | `0 2 8` | `id $` | `s5` |
| 8 | `0 2 8 5` | `$` | `r4 : L -> id` |
| 9 | `0 2 8 6` | `$` | `r5 : R -> L` |
| 10 | `0 2 8 9` | `$` | `r1 : S -> L=R` |
| 11 | `0 4` | `$` | `accept` |

#### Justification

The grammar is **not LR(0)** because state `I2` contains:

```text
S -> L . = R
R -> L .
```

So on look-ahead `=`, the parser can either:

1. shift `=` to continue `S -> L = R`, or
2. reduce `R -> L`

Hence there is a shift/reduce conflict, so the grammar is **not LR(0)**.

---

### (b) Handle pruning, bottom-up parsing of `aaa*a++`, and language generated [3 marks]

Handle pruning is the process used in bottom-up parsing where, at each step, the parser finds the handle of the current sentential form and reduces it to the corresponding non-terminal. By repeated reductions, the input is reduced back to the start symbol.

Given grammar:

```text
S -> SS+ | SS* | a
```

Input:

```text
aaa*a++
```

This grammar is a postfix-expression grammar.

#### Bottom-up shift-reduce parse

| Step | Stack | Input | Action |
|---|---|---|---|
| 1 | `$` | `aaa*a++$` | shift `a` |
| 2 | `$a` | `aa*a++$` | reduce `a -> S` |
| 3 | `$S` | `aa*a++$` | shift `a` |
| 4 | `$Sa` | `a*a++$` | reduce `a -> S` |
| 5 | `$SS` | `a*a++$` | shift `a` |
| 6 | `$SSa` | `*a++$` | reduce `a -> S` |
| 7 | `$SSS` | `*a++$` | shift `*` |
| 8 | `$SSS*` | `a++$` | reduce `SS* -> S` |
| 9 | `$SS` | `a++$` | shift `a` |
| 10 | `$SSa` | `++$` | reduce `a -> S` |
| 11 | `$SSS` | `++$` | shift `+` |
| 12 | `$SSS+` | `+$` | reduce `SS+ -> S` |
| 13 | `$SS` | `+$` | shift `+` |
| 14 | `$SS+` | `$` | reduce `SS+ -> S` |
| 15 | `$S` | `$` | accept |

#### Language generated

The grammar generates valid postfix expressions over:

1. operand `a`
2. binary operators `+` and `*`

Recursive definition of language:

```text
a is in L
if x and y are in L, then xy+ and xy* are in L
```

So the language is the set of postfix expressions formed from repeated operand `a` using binary `+` and `*`.

---

### (c) FIRST and FOLLOW sets [2 marks]

Grammar:

```text
S -> A B C D E
A -> a | epsilon
B -> b | epsilon
C -> c | epsilon
D -> d | epsilon
E -> e | epsilon
```

#### FIRST sets

```text
FIRST(A) = { a, epsilon }
FIRST(B) = { b, epsilon }
FIRST(C) = { c, epsilon }
FIRST(D) = { d, epsilon }
FIRST(E) = { e, epsilon }
FIRST(S) = { a, b, c, d, e, epsilon }
```

#### FOLLOW sets

```text
FOLLOW(S) = { $ }
FOLLOW(A) = { b, c, d, e, $ }
FOLLOW(B) = { c, d, e, $ }
FOLLOW(C) = { d, e, $ }
FOLLOW(D) = { e, $ }
FOLLOW(E) = { $ }
```

Reason: every symbol after `A` can disappear, so `$` also reaches `FOLLOW(A)`, and similarly for `B`, `C`, `D`.

---

## Q4

### (a) Keyword parameters and conditional assembly with example [2 marks]

#### Keyword parameters

In macro processors, keyword parameters are arguments passed by name, not only by position. They can also have default values.

Example:

```text
MACRO
INCR &ARG1, &REG=AREG
MOVER &REG, &ARG1
ADD   &REG, =1
MEND
```

Calls:

```text
INCR NUM
INCR NUM, &REG=BREG
```

Here `REG` is a keyword parameter with default value `AREG`.

#### Conditional assembly

Conditional assembly means the macro processor expands different statements depending on a condition known at assembly time.

Example:

```text
MACRO
COMPARE &X, &Y, &MODE=LT
AIF ('&MODE' EQ 'LT') LESS
MOVER AREG, &X
COMP  AREG, &Y
AGO   ENDL
LESS  MOVER BREG, &X
COMP  BREG, &Y
ENDL  MEND
```

Thus different code is generated depending on the value of `MODE`.

---

### (b) Branch to an external symbol in one-pass module assembler [2 marks]

In a one-pass module assembler, the address of an external symbol is not known during assembly. So, for a branch to an external symbol, the assembler does the following:

1. Enters the symbol in the external reference table.
2. Generates incomplete object code with a temporary value such as `0` in the address field.
3. Produces relocation or modification information saying that this field must later be corrected.
4. The linker/loader finally resolves the external symbol and patches the branch address.

So the one-pass assembler handles such branches using external reference entries plus relocation/modification records.

---

### (c) Compare different approaches to symbol table organization [3 marks]

Common approaches are:

| Approach | Lookup | Insertion | Advantages | Disadvantages |
|---|---|---|---|---|
| Linear list | `O(n)` | `O(1)` at end | Very simple | Slow search |
| Ordered list / array | `O(log n)` by binary search | `O(n)` | Easier searching than linear list | Insertions costly |
| Hash table | Average `O(1)` | Average `O(1)` | Very fast, most widely used | Collision handling needed |
| Tree (BST / balanced tree) | `O(log n)` average | `O(log n)` average | Maintains sorted order | More complex than hashing |

Comparison:

1. Linear tables are simple but inefficient for large programs.
2. Ordered tables improve searching but make insertion expensive.
3. Hash tables are best for compiler symbol tables because insertion and lookup are fast.
4. Trees are useful when ordered traversal is also required.

Hence, hash-table organization is generally preferred in compilers and assemblers.

---

### (d) Relocation bits and modification record [3 marks]

When a program is loaded at an address different from the one assumed during translation, address-dependent fields must be corrected. This is called relocation.

#### Relocation bits

Relocation bits are extra bits attached to object code words. Each bit tells whether the corresponding address field must be relocated.

Use:

1. `1` means relocate this field.
2. `0` means no relocation needed.

This method is simple and suitable when many fields need relocation.

#### Modification record

A modification record explicitly tells:

1. the starting location to be modified,
2. the length of the field,
3. sometimes the external symbol involved.

This is used mainly in loaders/linkers, especially when only a few fields need correction or when external references are present.

#### Difference

1. Relocation bits are compact for fixed-size object formats with many relocatable addresses.
2. Modification records are more flexible and are preferred when external symbols and variable-length address fields are involved.

---

## Final Conclusion

Important final results from this paper:

1. Q2(c): the grammar is **not LL(2)**.
2. Q3(a): the grammar is **not LR(0)** because of a shift/reduce conflict.
3. Q3(b): `aaa*a++` is accepted by bottom-up parsing.
