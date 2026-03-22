# System Software – Mid Semester Exam Solutions
**Exam:** March 2020
**Max Marks:** 30

---

## Q1

### 1. Language Processing Activities [3 marks]
Language processing involves the steps required to bridge the gap between application semantics and execution semantics. Major activities include:
1. **Program Generation:** Using application generators to produce source code from specifications.
2. **Program Translation:** Converting source code written in one language (like C or Assembly) into another (like Machine Code) using Compilers or Assemblers.
3. **Program Execution/Interpretation:** Executing the translated code or interpreting the source code line-by-line (using an Interpreter) to produce outputs from inputs.

### 2. Assembly Language Program Tables and Code [7 marks]
**Given Program Analysis & LC (Location Counter) Processing:**
* `START 205` $\to$ LC = 205
* `MOVER AREG, ='6'` $\to$ LC = 205
* `MOVEM AREG, A` $\to$ LC = 206
* `LOOP MOVER AREG, A` $\to$ LC = 207 **(LOOP = 207)**
* `MOVER CREG, B` $\to$ LC = 208
* `ADD CREG, ='2'` $\to$ LC = 209
* `BC ANY, NEXT` $\to$ LC = 210
* `LTORG` $\to$ **Pool 1:** `'6'` at 211, `'2'` at 212. LC becomes 213.
* `ADD BREG, B` $\to$ LC = 213
* `NEXT SUB AREG, ='1'` $\to$ LC = 214 **(NEXT = 214)**
* `BC LT, BACK` $\to$ LC = 215
* `LAST STOP` $\to$ LC = 216 **(LAST = 216)**
* `ORIGIN LOOP-3` $\to$ LC = 207 - 3 = 204
* `MULT CREG, B` $\to$ LC = 204
* `ORIGIN LAST+1` $\to$ LC = 216 + 1 = 217
* `A DS 1` $\to$ LC = 217 **(A = 217)**
* `BACK EQU LOOP` $\to$ **BACK = 207**
* `B DS 1` $\to$ LC = 218 **(B = 218)**
* `END` $\to$ **Pool 2:** `'1'` at 219.

**(b) Generated Tables [3 marks]:**
**SYMTAB**
| Symbol | Address |
| :--- | :--- |
| LOOP | 207 |
| NEXT | 214 |
| LAST | 216 |
| A | 217 |
| BACK | 207 |
| B | 218 |

**LITTAB**
| Literal | Address |
| :--- | :--- |
| ='6' | 211 |
| ='2' | 212 |
| ='1' | 219 |

**POOLTAB**
| Pool No | Starting LITTAB Index |
| :--- | :--- |
| 1 | 1 |
| 2 | 3 |

---

## Q2

### 1. Lexemes and Pattern OR Regular Expression [2 marks]
**Option 2 (Regular Expression & DFA):**
* **Regular Expression** for strings ending with "abb": `(a|b)*abb`
* **DFA Construction:** 
*(Requires 4 states. State q0 (start), q1 (sees 'a'), q2 (sees 'ab'), q3 (sees 'abb', accepting state). Transitions loop back appropriately on mismatched characters).*

### 2. Rightmost Derivation and Parse Tree [2 marks]
**Grammar:** $E \rightarrow E+T \mid E-T \mid T$, $T \rightarrow T*F \mid T/F \mid F$, $F \rightarrow id \mid (E)$
**Expression:** `(id * id) / id + id - id`

**Rightmost Derivation:**
$E \Rightarrow E - T$
$\Rightarrow E - F$
$\Rightarrow E - id$
$\Rightarrow E + T - id$
$\Rightarrow E + F - id$
$\Rightarrow E + id - id$
$\Rightarrow T + id - id$
$\Rightarrow T / F + id - id$
$\Rightarrow T / id + id - id$
$\Rightarrow F / id + id - id$
$\Rightarrow (E) / id + id - id$
$\Rightarrow (T) / id + id - id$
$\Rightarrow (T * F) / id + id - id$
$\Rightarrow (T * id) / id + id - id$
$\Rightarrow (F * id) / id + id - id$
$\Rightarrow (id * id) / id + id - id$


### 3. FIRST and FOLLOW for if-else [2 marks]
**Grammar:**
$S \rightarrow I \mid other$
$I \rightarrow if (E) S L$
$L \rightarrow else S \mid \epsilon$
$E \rightarrow 0 \mid 1$
*(Simplified variable names for clarity)*

* FIRST(S) = `{if, other}`
* FIRST(I) = `{if}`
* FIRST(L) = `{else, \epsilon}`
* FIRST(E) = `{0, 1}`
* FOLLOW(S) = `{$, else}`
* FOLLOW(L) = `{$, else}`

### 4. Left Factoring [2 marks]
**Grammar:** $S \rightarrow a \mid ab \mid abc \mid abcd$
**Eliminating Left Factoring:**
$S \rightarrow a A$
$A \rightarrow b B \mid \epsilon$
$B \rightarrow c C \mid \epsilon$
$C \rightarrow d \mid \epsilon$

### 5. LL(1) Parsing Table for Expression Grammar [4 marks]
**Grammar:**
$E \rightarrow T A$
$A \rightarrow + T A \mid \epsilon$
$T \rightarrow V B$
$B \rightarrow * V B \mid \epsilon$
$V \rightarrow id \mid (E)$

**FIRST Sets:**
FIRST(E) = FIRST(T) = FIRST(V) = `{id, (}`
FIRST(A) = `{+, \epsilon}`
FIRST(B) = `{*, \epsilon}`

**FOLLOW Sets:**
FOLLOW(E) = `{), $}`
FOLLOW(A) = `{), $}`
FOLLOW(T) = `{+, ), $}`
FOLLOW(B) = `{+, ), $}`
FOLLOW(V) = `{*, +, ), $}`

**Parsing Table entries:**
* `[E, id]` and `[E, (]` $\to$ $E \rightarrow TA$
* `[A, +]` $\to$ $A \rightarrow +TA$
* `[A, )]` and `[A, $]` $\to$ $A \rightarrow \epsilon$
* `[T, id]` and `[T, (]` $\to$ $T \rightarrow VB$
* `[B, *]` $\to$ $B \rightarrow *VB$
* `[B, +]`, `[B, )]`, `[B, $]` $\to$ $B \rightarrow \epsilon$
* `[V, id]` $\to$ $V \rightarrow id$
* `[V, (]` $\to$ $V \rightarrow (E)$

### 6. Phases of Compiler for $a = b * c + c * b$ [4 marks]

1.  **Lexical Analysis:** Output is a stream of tokens: `id1 = id2 * id3 + id3 * id2`.
2.  **Syntax Analysis:** Generates an Abstract Syntax Tree (AST) representing precedence (multiplications as children of addition).
3.  **Semantic Analysis:** Checks types. If variables are floats, inserts conversions (e.g., `inttofloat`). Output is an annotated AST.
4.  **Intermediate Code Gen:** `t1 = id2 * id3`
    `t2 = id3 * id2`
    `t3 = t1 + t2`
    `id1 = t3`
5.  **Code Optimization:** Recognizes `t1` and `t2` compute the same value (Common Subexpression Elimination). 
    `t1 = id2 * id3`
    `id1 = t1 + t1`
6.  **Target Code Generation:** Assembly code generation (e.g., `MOV R1, id2`, `MUL R1, id3`, `ADD R1, R1`, `MOV id1, R1`).