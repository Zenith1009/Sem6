
### System Software – Mid Semester Examination

**SVNIT, Surat** <br>
**Course:** CO304 – System Software <br>
**Exam:** Mid Semester Examination – March 2020 <br>
**Time:** 14:00 – 15:30 <br>
**Max Marks:** 30

Date: 03-03-2020

---

# Q1. Answer the following (10 Marks)

## 1. Explain Language Processing Activities.

**Marks:** 3

---

## 2. Consider the following Assembly Language Program

```
START   205
MOVER   AREG, ='6'
MOVEM   AREG, A

LOOP    MOVER   AREG, A
        MOVER   CREG, B
        ADD     CREG, ='2'
        BC      ANY, NEXT
        LTORG

        ADD     BREG, B

NEXT    SUB     AREG, ='1'
        BC      LT, BACK

LAST    STOP
        ORIGIN  LOOP-3
        MULT    CREG, B

        ORIGIN  LAST+1
A       DS      1

BACK    EQU     LOOP
B       DS      1
END
```

### Answer the following:

a) Generate **Intermediate Code** and **Target Code**
**Marks:** 4

b) Generate the following tables:

* **SYMTAB**
* **LITTAB**
* **POOLTAB**

**Marks:** 3

---

# Q2. Answer the following (20 Marks)

## 1. Define the following terms:

a) **Lexemes**
b) **Pattern**

**Marks:** 2

### OR

Write **Regular Expressions** for all strings ending with **"abb"** and construct the **equivalent DFA**.

**Marks:** 2

---

## 2. Consider the following grammar:

```
E → E + T | E − T | T
T → T * F | T / F | F
F → id | (E)
```

Derive the expression:

```
(id * id) / id + id − id
```

using **rightmost derivation**. Also draw the **parse tree** for the same.

**Marks:** 2

---

## 3. Find **FIRST and FOLLOW** set for the following grammar:

```
statement → if-stmt | other
if-stmt   → if (exp) statement else-part
else-part → else statement | ε
exp       → 0 | 1
```

**Marks:** 2

---

## 4. Eliminate **Left Recursion**, if any, from the following grammar:

```
A → Br
A → x
B → Cs
B → y
C → At
C → z
```

### OR

Define **Left Factoring**. Eliminate left factoring from the following grammar:

```
S → a | ab | abc | abcd
```

**Marks:** 2

---

## 5. Develop an **LL(1) parsing table** for the following grammar and parse the string 
`(id * id) + (id * id)`

Grammar:

```
E → T A
A → + T A | ε
T → V B
B → * V B | ε
V → id | (E)
```

### OR

Draw **LL(1) predictive parsing table** for the following grammar and trace the execution for input `bdcea`

Grammar:

```
S → Aa | b
A → bdC | C
C → abC | cC | ε
```

**Marks:** 4

---

## 6. Explain **various phases of the compiler** in detail.
Also write the **output of the following expression after each phase**.
`a = b * c + c * b`

**Marks:** 4

---

## 7. Design **LL(1) parsing table** for the following grammar:

```
bexpr  → bexpr or bterm | bterm
bterm  → bterm and bfactor | bfactor
bfactor → not bfactor | (bexpr) | true | false
```

**Marks:** 4

---

**End of Paper**