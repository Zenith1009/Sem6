# System Software – Mid Semester Exam Solutions

**Exam:** March 2023 <br>
**Max Marks:** 30

---

## Q.1 

### 1. Macro Assembler Concepts [4 marks]
* **Generation Time Activities:** These are operations performed by the macro pre-processor during the expansion of a macro, rather than at execution time. Example: Evaluating mathematical expressions to generate specific instructions or expanding a loop `N` times based on a parameter.
* **Keyword Parameters:** Parameters passed to a macro using their name rather than their positional order. They allow default values. Example: `MACRO_NAME &PARAM1=10`.
* **Expansion Time Variables (EVs):** Variables used within the macro definition that are assigned values and evaluated during macro expansion. They are often used to control conditional assembly or loops (e.g., `&COUNT SET 0`).
* **Conditional Assembly:** The use of pre-processor directives (like `AIF`, `AGO`) to include or exclude certain blocks of assembly code from the final expanded output based on logical conditions evaluated at generation time. 

### 2. Symbol Table Organization Approaches [3 marks]
| Feature | Linear List (Array/Linked List) | Binary Search Tree (BST) | Hash Table |
| :--- | :--- | :--- | :--- |
| **Search Time** | $O(N)$ (slow) | $O(\log N)$ (average) | $O(1)$ (fastest average) |
| **Insertion Time**| $O(1)$ for unsorted | $O(\log N)$ | $O(1)$ |
| **Implementation**| Very simple | Moderate complexity | Complex (requires good hash function & collision handling like chaining) |
| **Use Case** | Small programs/modules | Medium-sized programs | Standard for modern, large-scale compilers |

### 3. One Pass Macro Pre-Processor Flowchart [3 marks]
A one-pass macro processor handles definition and expansion in a single pass. 

**Explanation:** 1. Read the next line of source code.
2. If it's a `MACRO` pseudo-op, enter the **definition mode**: read lines and store them in the Macro Definition Table (MDT) and record the name in the Macro Name Table (MNT) until `MEND` is found.
3. If it matches a name in the MNT, enter **expansion mode**: substitute arguments for parameters and output the lines from the MDT.
4. Otherwise, write the source line directly to the expanded output file.

---

## Q.2

### 1. NFA and DFA for $a(a|b)*ab$ [3 marks]
**Regular Expression:** $a(a|b)*ab$


*(Note: To construct this on paper, draw an initial state transitioning on 'a' to a loop state. The loop state loops on both 'a' and 'b'. From the loop state, transition on 'a' to a sub-final state, and from there transition on 'b' to the final accept state. The DFA subset construction will determinize the non-deterministic jump on 'a')*.

### 2. Analysis and Synthesis Phases [2 marks]
* **Analysis Phase (Front-end):** Breaks down the source code into its constituent pieces and creates an intermediate representation. Includes Lexical, Syntax, and Semantic analysis. Example: Checking if `x = y + z` is syntactically valid and if `y` and `z` have compatible types.
* **Synthesis Phase (Back-end):** Takes the intermediate representation and generates the target machine code. Includes Code Optimization and Target Code Generation. Example: Converting the validated intermediate code into optimized assembly like `ADD R1, R2`.

### 3. Top Down Parsing and Recursive Descent with Backtracking [3 marks]
* **Top-Down Parsing:** A parsing strategy that builds the parse tree from the root (start symbol) down to the leaves (terminals) by applying grammar productions recursively.
* **Recursive Descent with Backtracking:** A brute-force top-down parsing method. It tries to apply productions one by one. If a chosen production fails to match the input string halfway through, the parser "backtracks" (undoes the consumed input and tree generation) and tries the next alternative production.
* **Example:** For $S \rightarrow cad \mid cbc$, and input `cbc`. The parser first tries $S \rightarrow cad$. It matches `c`, but `a` fails to match `b`. It backtracks the input pointer to `b` and tries the next production $S \rightarrow cbc$, which succeeds.

### 4. LR(1) DFA from Parse Table [6 marks]
**Grammar:** $S \rightarrow L=R \mid R$, $L \rightarrow *R \mid id$, $R \rightarrow L$
Using the provided parsing table, the DFA transitions are derived from the Shift (`s`) and Goto entries:

* **State 0:** Transitions on `id` $\to$ 5, `*` $\to$ 4, `S` $\to$ 1, `L` $\to$ 2, `R` $\to$ 3.
* **State 2:** Transition on `=` $\to$ 6.
* **State 4:** Transitions on `id` $\to$ 5, `*` $\to$ 4, `L` $\to$ 8, `R` $\to$ 7.
* **State 6:** Transitions on `id` $\to$ 12, `*` $\to$ 11, `L` $\to$ 10, `R` $\to$ 9.
* **State 11:** Transitions on `id` $\to$ 12, `*` $\to$ 11, `L` $\to$ 10, `R` $\to$ 13.

### 5. FIRST, FOLLOW, and LL(1) Parsing [6 marks]
**Grammar:**
$Expr \rightarrow -Expr \mid (Expr) \mid Var\ ExprTail$
$ExprTail \rightarrow -Expr \mid \epsilon$
$Var \rightarrow ID\ VarTail$
$VarTail \rightarrow (Expr) \mid \epsilon$

**1. FIRST and FOLLOW sets:**
* FIRST(Expr) = `{-, (, ID}`
* FIRST(ExprTail) = `{-, \epsilon}`
* FIRST(Var) = `{ID}`
* FIRST(VarTail) = `{(, \epsilon}`
* FOLLOW(Expr) = `{$, ), -}`
* FOLLOW(ExprTail) = `{$, ), -}`
* FOLLOW(Var) = `{-, $, )}`
* FOLLOW(VarTail) = `{-, $, )}`

*(The LL(1) table maps productions to the intersection of Non-terminals and Terminals based on the FIRST sets, and places $\epsilon$-productions under the FOLLOW set terminals)*.