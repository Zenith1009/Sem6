# System Software – Mid Semester Exam Solutions
**Exam:** September 2024
**Max Marks:** 30

---

## Q1

### (a) Role of Lexical Analyser and Why it is a Separate Phase [2 marks]
**Role:** The lexical analyzer (scanner) reads the stream of characters making up the source program and groups them into meaningful sequences called **lexemes**. For each lexeme, it produces a **token** of the form `<token-name, attribute-value>` that it passes on to the parser for syntax analysis. It also strips out whitespaces and comments, and correlates error messages with source program line numbers.

**Why it is implemented as a separate phase:**
1. **Simplified Design:** It simplifies the parser's design since the parser does not have to deal with low-level details like whitespace and comments.
2. **Compiler Efficiency:** Specialized buffering techniques can be applied to reading characters to speed up the compiler.
3. **Compiler Portability:** Input-device-specific anomalies can be restricted to the lexical analyzer, making the rest of the compiler more portable.

### (b) Techniques to Look-Ahead on the Input (Input Buffering) [2 marks]
To identify tokens effectively without making excessive system I/O calls, compilers use **input buffering schemes**:
1. **One-Buffer Scheme:** A single buffer is used to load a block of characters. However, if a lexeme spans across the end of the buffer, it causes complications requiring the buffer to be reloaded prematurely.
2. **Two-Buffer Scheme (with Sentinels):** Two buffers of equal size are used. Two pointers, `lexemesBegin` and `forward`, traverse the input. The `forward` pointer moves ahead to find the end of the token. To avoid checking if the pointer has reached the end of the buffer on every single character move, a **sentinel character** (usually `EOF`) is placed at the end of each buffer half. This significantly optimizes the look-ahead process.

---

## Q2

### (a) Eliminate Left Recursion and Left Factor [2 marks]
**Given Grammar:**
$E \rightarrow aba \mid abba \mid Ea \mid EbE$

**Step 1: Eliminate Left Recursion**
Group the productions into left-recursive and non-left-recursive parts:

$E \rightarrow E \alpha_1 \mid E \alpha_2 \mid \beta_1 \mid \beta_2$

Where: $\alpha_1 = a$, $\alpha_2 = bE$, $\beta_1 = aba$, $\beta_2 = abba$

Using the standard elimination rule:

$E \rightarrow aba E' \mid abba E'$

$E' \rightarrow a E' \mid b E E' \mid \epsilon$

**Step 2: Left Factoring**
Look at the productions for $E$. Both start with the common prefix $ab$.
$E \rightarrow abX$
$X \rightarrow aE' \mid baE'$

*(The grammar is now both free of left-recursion and left-factored).*

### (b) Ambiguity and Unambiguous Grammar [3 marks]
**Given Grammar:**
$E \rightarrow E + E \mid E * E \mid (E) \mid id$

**1. Show Ambiguity:**
A grammar is ambiguous if there is more than one parse tree (or leftmost derivation) for the same string.
Consider the string: `id + id * id`
* **Tree 1 (Evaluating `*` first):** $E \Rightarrow E + E \Rightarrow id + E * E \Rightarrow id + id * id$
* **Tree 2 (Evaluating `+` first):** $E \Rightarrow E * E \Rightarrow E + E * E \Rightarrow id + id * id$
Since two different parse trees exist, the grammar is ambiguous.

**2. Unambiguous Grammar (with `+` having higher priority and both left-associative):**
To give `+` higher priority, we place it lower in the parse tree (closer to the terminals).
$E \rightarrow E * T \mid T$
$T \rightarrow T + F \mid F$
$F \rightarrow (E) \mid id$

### (c) LL(2) Predictive Parse Table Check [3 marks]
**Given Grammar:**
$X \rightarrow XSb \mid Sa \mid b$
$S \rightarrow Sb \mid Xa \mid a$

**Analysis:**
Notice the production $X \rightarrow XSb$. This is **immediate left recursion**. 
A top-down parser (like an LL parser) processes input left-to-right. If a grammar has left recursion, the parser will enter an infinite loop trying to expand $X$ into $XSb$ without ever consuming any input characters. 
**Conclusion:** Therefore, the grammar **cannot be LL(2)** (or LL(k) for any k) in its current form. 
**Steps to construct a table (which would fail here):**
1. Eliminate left recursion.
2. Perform left factoring if needed.
3. Compute FIRST and FOLLOW sets.
4. Construct the predictive parsing table. Without step 1, table construction will yield multiple entries (conflicts) for the same cell, proving it is not LL(k).

---

## Q3

### (a) Canonical Collection of LR(0) Items and Parsing [3 marks]
**Given Grammar:**
1. $S \rightarrow L = R$
2. $S \rightarrow R$
3. $L \rightarrow * R$
4. $L \rightarrow id$
5. $R \rightarrow L$

**Augmented Grammar:** $S' \rightarrow S$

**LR(0) Item Sets:**
* **I0:** $S' \rightarrow .S$, $S \rightarrow .L=R$, $S \rightarrow .R$, $L \rightarrow .*R$, $L \rightarrow .id$, $R \rightarrow .L$
* **I1:** $S' \rightarrow S.$ (Accept)
* **I2:** $S \rightarrow L.=R$, $R \rightarrow L.$
* **I3:** $S \rightarrow R.$
* **I4:** $L \rightarrow *.R$, $R \rightarrow .L$, $L \rightarrow .*R$, $L \rightarrow .id$
* **I5:** $L \rightarrow id.$
* **I6:** $S \rightarrow L=.R$, $R \rightarrow .L$, $L \rightarrow .*R$, $L \rightarrow .id$
* **I7:** $L \rightarrow *R.$
* **I8:** $R \rightarrow L.$
* **I9:** $S \rightarrow L=R.$

**LR(0) Parsing Table Conflict & Justification:**
In State **I2**, we have two items:
1. $S \rightarrow L.=R$ (Shift on `=`)
2. $R \rightarrow L.$ (Reduce on anything)
Because LR(0) does not look ahead to resolve conflicts, State I2 contains a **Shift/Reduce conflict**. Therefore, **the grammar is NOT LR(0)**.

*(Note: Parsing `*id = id` requires resolving the conflict by choosing Shift, which effectively makes it an SLR(1) parse. LR(0) would fail deterministically here).*

### (b) Handle Pruning [3 marks]
**Handle Pruning:** A "handle" is a substring that matches the right side of a production and whose reduction to the non-terminal on the left side represents one step along the reverse of a rightmost derivation. Handle pruning is the process of locating handles and reducing them to their corresponding LHS non-terminal to build the parse tree bottom-up.

**Given Grammar:** $S \rightarrow SS+ \mid SS* \mid a$
**Input:** `aaa*a++`

**Bottom-Up Parser Trace:**
| Stack | Input | Action |
| :--- | :--- | :--- |
| `$` | `aaa*a++$` | Shift `a` |
| `$a` | `aa*a++$` | Reduce $S \rightarrow a$ |
| `$S` | `aa*a++$` | Shift `a` |
| `$Sa` | `a*a++$` | Reduce $S \rightarrow a$ |
| `$SS` | `a*a++$` | Shift `a` |
| `$SSa` | `*a++$` | Reduce $S \rightarrow a$ |
| `$SSS` | `*a++$` | Shift `*` |
| `$SSS*`| `a++$` | Reduce $S \rightarrow SS*$ |
| `$SS` | `a++$` | Shift `a` |
| `$SSa` | `++$` | Reduce $S \rightarrow a$ |
| `$SSS` | `++$` | Shift `+` |
| `$SSS+`| `+$` | Reduce $S \rightarrow SS+$ |
| `$SS` | `+$` | Shift `+` |
| `$SS+` | `$` | Reduce $S \rightarrow SS+$ |
| `$S` | `$` | Accept |

**Language Generated:** The grammar generates mathematical expressions containing operand 'a' and binary operators '+' and '*' written in **Postfix Notation**.

### (c) FIRST and FOLLOW Sets [2 marks]
**Grammar:**
$S \rightarrow ABCDE$
$A \rightarrow a \mid \epsilon$
$B \rightarrow b \mid \epsilon$
$C \rightarrow c \mid \epsilon$
$D \rightarrow d \mid \epsilon$
$E \rightarrow e \mid \epsilon$

**FIRST Sets:**
* FIRST(A) = `{a, ε}`
* FIRST(B) = `{b, ε}`
* FIRST(C) = `{c, ε}`
* FIRST(D) = `{d, ε}`
* FIRST(E) = `{e, ε}`
* FIRST(S) = `{a, b, c, d, e, ε}` *(Since A, B, C, D, E can all derive ε)*

**FOLLOW Sets:**
* FOLLOW(S) = `{$}`
* FOLLOW(A) = `{b, c, d, e, $}`
* FOLLOW(B) = `{c, d, e, $}`
* FOLLOW(C) = `{d, e, $}`
* FOLLOW(D) = `{e, $}`
* FOLLOW(E) = `{$}`

---

## Q4

### (a) Keyword Parameters and Conditional Assembly [2 marks]
* **Keyword Parameters:** In a macro assembler, parameters can be assigned by name rather than their positional sequence. Example: `MACRO_NAME &PARAM1=10, &PARAM2=20`. This allows programmers to omit default parameters and specify only what they want to change.
* **Conditional Assembly:** Directives (like `AIF`, `AGO` in some assemblers) allow the macro processor to conditionally include or skip blocks of code during expansion based on boolean conditions. Example: Expanding a macro for a 32-bit addition versus a 64-bit addition depending on a passed parameter.

### (b) One-Pass Module Assembler and External Symbols [2 marks]
A one-pass assembler resolves branches to external symbols by using **Modification Records** (or a fix-up chain). When it encounters a branch to an external symbol, it cannot know the target address. It outputs a dummy address (like `0000`) in the object code and writes a Modification Record to the object file. The Linker/Loader later reads this record and "patches" the dummy address with the correctly resolved external address at load time.

### (c) Symbol Table Organisation Approaches [3 marks]
1.  **Linear List (Arrays/Linked Lists):** Simple to implement and memory efficient for small programs. Search is slow ($O(N)$), while insertion is fast ($O(1)$).
2.  **Binary Search Trees:** Offers a balanced approach with $O(\log N)$ for both searching and insertion, provided the tree remains balanced. Complex to maintain balancing during rapid insertions.
3.  **Hash Tables:** The most widely used approach in modern compilers. Offers $O(1)$ average time complexity for both insertions and lookups, though it requires resolving collisions (e.g., using separate chaining).

### (d) Relocation Bits and Modification Record [3 marks]
* **Relocation Bits:** A bitmask generated by the assembler associated with a text record. A value of `1` indicates that the corresponding memory word contains an address that needs to be relocated (adjusted by the starting load address of the program) by the loader.
* **Modification Record:** Used heavily in object files (like ELF or standard IBM formats) to tell the linker/loader explicitly where an address modification is required. It typically contains the starting address of the field to modify, the length of the field, and the external symbol or segment whose address needs to be added/subtracted.