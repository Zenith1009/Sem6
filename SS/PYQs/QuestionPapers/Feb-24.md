
# System Software – Mid Semester Exam

**SVNIT, Surat** <br>
**Course:** CS306 – System Software <br>
**Exam:** Mid Semester Examination – February 2024 <br>
**Date:** 28-02-2024 <br>
**Time:** 2:00 PM – 3:30 PM <br>
**Max Marks:** 30

---

# Q1

### 1. 

Explain the following with example (any two):

- OPTAB
- SYMTAB
- LITAB
- POOLTAB

**[2 marks]**

---

### 2. 

Discuss **language processing activities**.
OR
Write a **LEX program** for removing comments in a C program.

**[2 marks]**

---

### 3

Write a **macro** that takes parameters **A, B, C, D** and calculates:

```
A * B + C * D
```

Result stored in **AREG**. Also mention the **types of parameters used**.
Example: `AREG` is the **default parameter**.

**[2 marks]**

---

### 4. 

Given the source program:

```
START 200
MOVER AREG, =5
MOVEM AREG, M

L1   MOVER AREG, =2
     ORIGIN L1+3
     LTORG

NEXT ADD AREG, =1
     SUB BREG, =2
     BC LT, BACK
     LTORG

BACK EQU L1
     ORIGIN NEXT+5
     MULT CREG, =4
     STOP

X    DS 2
END
```

Tasks:

1. Show the **Symbol Table** generated at the end of **Pass I**.
2. Show the **Intermediate Code** generated for the program.

**[4 marks]**

---

# Q2

## 1. [5 marks]

Write **FIRST and FOLLOW sets** and construct a **predictive parsing table** for:

```
E → TA
A → +TA | -TA | ε
T → FB
B → *FB | /FB | ε
F → -S | S
S → v | (E)
```

Show parsing action for input string:

```
(v+v)
```

---

## 2. [3 marks]

Construct **NFA and DFA** for:

```
a(ab)*a
```

OR

Give **transition diagram** for recognizing:

* comments
* identifiers in C

---

## 3. [4 marks]

Check whether the grammar is **LL(1)**.

```
S → 0 | 1S2S3 | 1A3
A → S | AS
```

Construct predictive parsing table and explain steps.

---

## 4. [2 marks]

Eliminate **left recursion** and perform **left factoring**.

```
S → A
A → Ad | Ae | aB | ac
B → bBc | f
```

---

## 5. [4 marks]

### (a)

Define:

* Tokens
* Lexemes
* Pattern

### (b)

Find total **number of lexemes** in:

```c
#include
#include

int main()
{
    printf("%d + %d = %d",3,1,4); /*sum*/
    return 0;
}
```

---

## 6. [2 marks]

Check whether the grammar is **ambiguous** for string:

```
aabbccdd
```

Grammar:

```
S → AB | C
A → aAb | ab
B → cBd | cd
C → aCd | aDd
D → bDc | bc
```
