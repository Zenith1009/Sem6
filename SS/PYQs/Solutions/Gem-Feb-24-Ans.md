# System Software – Mid Semester Exam Solutions
**Exam:** February 2024
**Max Marks:** 30

---

## Q1

### 1. Explain tables with examples [2 marks] (Any two required, all four provided for study)
* **OPTAB (Operation Code Table):** Maps assembly mnemonics to their machine language opcodes and instruction formats. Example: `ADD` maps to opcode `18` with format `RX`.
* **SYMTAB (Symbol Table):** Stores labels/symbols defined in the program along with their assigned memory addresses (Location Counter values). Example: Label `LOOP` mapped to address `205`.
* **LITAB (Literal Table):** Stores all literals used in the program and the addresses assigned to them during literal pool allocation. Example: `=5` assigned to address `205`.
* **POOLTAB (Pool Table):** Keeps track of the starting index of each literal pool within the LITAB. Example: Pool 2 starts at LITAB index #3.

### 2. LEX program for removing C comments [2 marks]
```lex
%%
"//".* { /* Match single-line comments and ignore */ }
"/*"([^*]|\*+[^*/])*\*+"/" { /* Match multi-line comments and ignore */ }
.|\n                    { printf("%s", yytext); /* Print everything else */ }
%%
int yywrap() { return 1; }

```

### 3. Macro calculating A * B + C * D [2 marks]

```assembly
MACRO
CALC &A, &B, &C, &D, &REG=AREG
MOVER &REG, &A
MULT &REG, &B
MOVEM &REG, TEMP
MOVER CREG, &C
MULT CREG, &D
ADD &REG, CREG
MEND

```

**Types of parameters used:**

* `&A, &B, &C, &D` are **Positional Parameters**.
* `&REG=AREG` is a **Keyword Parameter** with a **Default Value** (`AREG`).

### 4. Given Source Program: Symbol Table and Intermediate Code [4 marks]

**Location Counter (LC) Processing:**

* `START 200` (LC = 200)
* `MOVER AREG, =5` (200)
* `MOVEM AREG, M` (201)
* `L1 MOVER AREG, =2` (202) -> **L1=202**
* `ORIGIN L1+3` (LC = 202+3 = 205)
* `LTORG` -> Pool 1: `=5` at **205**, `=2` at **206**. (LC becomes 207).
* `NEXT ADD AREG, =1` (207) -> **NEXT=207**
* `SUB BREG, =2` (208)
* `BC LT, BACK` (209)
* `LTORG` -> Pool 2: `=1` at **210**, `=2` at **211**. (LC becomes 212).
* `BACK EQU L1` -> **BACK=202**
* `ORIGIN NEXT+5` (LC = 207+5 = 212)
* `MULT CREG, =4` (212)
* `STOP` (213)
* `X DS 2` (214) -> **X=214**. (Size 2, LC becomes 216).
* `END` -> Pool 3: `=4` at **216**.

**1. Symbol Table (SYMTAB):**
| Symbol | Address |
| :--- | :--- |
| L1 | 202 |
| NEXT | 207 |
| BACK | 202 |
| X | 214 |
| M | *(Undefined/External)* |

**2. Intermediate Code (Snippet - Pass 1 structure):**
*(Note: Using generic declarative notation (IS=Instruction, DL=Declarative, AD=Assembler Directive, C=Constant, S=Symbol, L=Literal))*

* `(AD, 01) (C, 200)`
* `(IS, 04) (RG, 01) (L, 01)`  *(MOVER AREG, =5)*
* `(IS, 05) (RG, 01) (S, 05)`  *(MOVEM AREG, M)*
* `L1 (IS, 04) (RG, 01) (L, 02)` *(MOVER AREG, =2)*
* ... *(continues matching instructions to class/opcodes)*

---

## Q2

### 1. FIRST, FOLLOW, and Predictive Parsing [5 marks]

**Grammar:**
$E \rightarrow TA$
$A \rightarrow +TA \mid -TA \mid \epsilon$
$T \rightarrow FB$
$B \rightarrow *FB \mid /FB \mid \epsilon$
$F \rightarrow -S \mid S$
$S \rightarrow v \mid (E)$

**FIRST Sets:**

* FIRST(S) = `{v, (}`
* FIRST(F) = `{-, v, (}`
* FIRST(T) = `{-, v, (}`
* FIRST(E) = `{-, v, (}`
* FIRST(A) = `{+, -, ε}`
* FIRST(B) = `{*, /, ε}`

**FOLLOW Sets:**

* FOLLOW(E) = `{$, )}`
* FOLLOW(A) = `{$, )}`
* FOLLOW(T) = `{+, -, $, )}`
* FOLLOW(B) = `{+, -, $, )}`
* FOLLOW(F) = `{*, /, +, -, $, )}`
* FOLLOW(S) = `{*, /, +, -, $, )}`

*(The predictive parsing table is constructed by mapping $A \rightarrow \alpha$ to cell `[A, a]` where `a` is in FIRST($\alpha$), and to FOLLOW(A) if $\alpha$ derives $\epsilon$)*.

### 2. NFA and DFA for `a(ab)*a` [3 marks]

*Construction approach:*

1. **Start State (q0):** Transition on `a` to State `q1`.
2. **Loop State (q1):** To handle `(ab)*`, create a transition on `a` to `q2`, and from `q2` transition on `b` back to `q1`.
3. **Accept State (q3):** From `q1`, transition on `a` to the final accept state `q3`.
*(Note: You would draw the circles and arrows directly on the paper based on these exact subset transitions).*

### 3. Check LL(1) [4 marks]

**Grammar:**
$S \rightarrow 0 \mid 1S2S3 \mid 1A3$
$A \rightarrow S \mid AS$

**Checking LL(1) Condition:**
For a grammar to be LL(1), the FIRST sets of all RHS alternatives for a given non-terminal must be disjoint.
Look at $S \rightarrow 1S2S3$ and $S \rightarrow 1A3$.

* FIRST($1S2S3$) = `{1}`
* FIRST($1A3$) = `{1}`
Since the intersection of these two sets is `{1}` (not empty), the grammar has a FIRST/FIRST conflict. Therefore, the grammar is **NOT LL(1)**.

### 4. Eliminate Left Recursion and Left Factor [2 marks]

**Grammar:**
$S \rightarrow A$
$A \rightarrow Ad \mid Ae \mid aB \mid ac$
$B \rightarrow bBc \mid f$

**1. Left Recursion (in A):**
$A \rightarrow aBA' \mid acA'$
$A' \rightarrow dA' \mid eA' \mid \epsilon$

**2. Left Factoring (in A):**
$A \rightarrow aX$
$X \rightarrow BA' \mid cA'$

### 5. Tokens, Lexemes, Pattern & Lexeme Count [4 marks]

**(a) Definitions:**

* **Tokens:** A classification or category of a lexeme (e.g., `IDENTIFIER`, `KEYWORD`, `OPERATOR`).
* **Lexemes:** The actual sequence of characters in the source code that matches the pattern for a token (e.g., `int`, `count`, `+`).
* **Pattern:** The rule or regular expression that describes how a sequence of characters can form a specific token.

**(b) Lexeme count in C code:**
Ignoring preprocessor directives and comments (which the lexical analyzer strips/handles via rules):
`int`, `main`, `(`, `)`, `{`, `printf`, `(`, `"%d + %d = %d"`, `,`, `3`, `,`, `1`, `,`, `4`, `)`, `;`, `return`, `0`, `;`, `}`
**Total Lexemes:** 20.

### 6. Ambiguity for string `aabbccdd` [2 marks]

**Grammar:**
$S \rightarrow AB \mid C$
$A \rightarrow aAb \mid ab$
$B \rightarrow cBd \mid cd$
$C \rightarrow aCd \mid aDd$
$D \rightarrow bDc \mid bc$

To check if it is ambiguous, we see if `aabbccdd` has more than one leftmost derivation:

1. **Derivation via AB:** $S \Rightarrow AB \Rightarrow aAbB \Rightarrow aabbB \Rightarrow aabbcBd \Rightarrow aabbccdd$
2. **Derivation via C:** $S \Rightarrow C \Rightarrow aCd \Rightarrow aaDdd \Rightarrow aabDcdd \Rightarrow aabbccdd$

Since the same string can be derived through two completely different leftmost derivation paths (one passing through $AB$ and one through $C$), the grammar is **ambiguous**.
