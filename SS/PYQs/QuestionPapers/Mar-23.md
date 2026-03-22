
# System Software – Mid Semester Exam

**SVNIT, Surat** <br>
**Course:** CS306 – System Software <br>
**Exam:** Mid Semester Examination – March 2023

---

## Questions

### System Software – Mid Semester Examination

**SVNIT, Surat**
**Course:** CS306 – System Software
**Exam:** Mid Semester Examination – March 2023
**Max Marks:** 30

---

## Q.1 Answer the following:

### 1. Explain with example 
- generation time activities
- keyword parameters
- expansion time variables
- conditional assembly with respect to macro assembler.

**Marks:** 04

---

### 2. Compare and contrast between various approaches to symbol table organization.

**Marks:** 03

---

### 3. Draw and explain flowchart for One Pass Macro Pre-Processor without nested macro calls.

**Marks:** 03



## Q.2 Answer the following:

### 1. Convert the following Regular Expression into NFA and DFA

```
a(a|b)*ab
```

**Marks:** 03

---

### 2. Explain analysis and synthesis phases of compiler with example.

**Marks:** 02

---

### 3. What do you mean by Top Down Parsing? Explain **Recursive Descent Parsing using Backtracking** with example.

**Marks:** 03

---

### 4. Draw the LR(1) DFA from the given grammar and parse table

#### Grammar G

```
S → L = R
S → R
L → *R
L → id
R → L
```

#### Parsing Table

| State | id  | *   | =  | $   | S | L  | R  |
| ----- | --- | --- | -- | --- | - | -- | -- |
| 0     | s5  | s4  |    |     | 1 | 2  | 3  |
| 1     |     |     |    | acc |   |    |    |
| 2     |     |     | s6 | r5  |   |    |    |
| 3     |     |     |    | r2  |   |    |    |
| 4     | s5  | s4  |    |     |   | 8  | 7  |
| 5     |     |     | r4 | r4  |   |    |    |
| 6     | s12 | s11 |    |     |   | 10 | 9  |
| 7     |     |     | r3 | r3  |   |    |    |
| 8     |     |     | r5 | r5  |   |    |    |
| 9     |     |     |    | r1  |   |    |    |
| 10    |     |     |    | r5  |   |    |    |
| 11    | s12 | s11 |    |     |   | 10 | 13 |
| 12    |     |     |    | r4  |   |    |    |
| 13    |     |     |    | r3  |   |    |    |

**Marks:** 06

---

### 5. For the following grammar

1. Calculate **FIRST and FOLLOW** of each non-terminal
2. Construct **LL(1) parsing table**
3. Parse the input string:

```
ID -- ID((ID))
```

#### Grammar

```
Expr     → -Expr | (Expr) | Var ExprTail
ExprTail →  -Expr | ε
Var      → ID VarTail
VarTail  → (Expr) | ε
```

**Marks:** 06