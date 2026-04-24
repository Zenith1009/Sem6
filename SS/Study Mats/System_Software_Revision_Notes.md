# System Software Revision Notes

SVNIT-style quick revision sheet for major System Software concepts.  
Use this as a last-minute concept recap, not as a full answer book.

---

## 1. Language Processing System

### Basic flow

```text
Source Program -> Preprocessor -> Compiler -> Assembler -> Linker -> Loader -> Execution
```

### Main roles

1. Preprocessor:
   Expands macros, includes files, removes comments, handles conditional compilation.
2. Compiler:
   Converts high-level language to assembly or intermediate code.
3. Assembler:
   Converts assembly language to machine code.
4. Linker:
   Combines object modules and libraries, resolves external references.
5. Loader:
   Loads executable into memory and starts execution.

### One-line exam definition

Language processing activities are the sequence of translation steps used to convert a source program into an executable machine-level program.

---

## 2. Compiler Phases

### Front end and back end

1. Analysis phase = front end.
2. Synthesis phase = back end.

### Phases in order

1. Lexical analysis
2. Syntax analysis
3. Semantic analysis
4. Intermediate code generation
5. Code optimization
6. Target code generation

### Output after each phase for `a = b * c + c * b`

#### Lexical analysis

```text
id(a) = id(b) * id(c) + id(c) * id(b)
```

#### Syntax analysis

Builds parse tree / syntax tree according to precedence.

#### Intermediate code

```text
t1 = b * c
t2 = c * b
t3 = t1 + t2
a  = t3
```

#### Optimized code

```text
t1 = b * c
t2 = t1 + t1
a  = t2
```

#### Target code idea

```text
MOV R1, b
MUL R1, c
ADD R1, R1
MOV a, R1
```

### Key difference

1. Analysis phase checks and understands the source program.
2. Synthesis phase generates efficient target code.

---

## 3. Lexical Analysis

### Important terms

1. Token:
   Category of lexical unit, such as `id`, `num`, `if`, `+`.
2. Lexeme:
   Actual character sequence matching a token.
3. Pattern:
   Rule describing all lexemes for a token.

### Example

```text
Token   : id
Lexeme  : count
Pattern : letter (letter | digit)*
```

### Role of lexical analyser

1. Reads source program character by character.
2. Groups characters into tokens.
3. Removes white spaces and comments.
4. Enters identifiers/literals in symbol table.
5. Reports lexical errors.

### Why it is a separate phase

1. Makes compiler modular.
2. Speeds up syntax analysis.
3. Simplifies parser design.
4. Handles buffering and token recognition efficiently.

### Input buffering schemes

1. Single buffer.
2. Sentinel scheme.
3. Double buffer with sentinels.

Most important answer:

```text
Two-buffer scheme with sentinels is the standard efficient method.
```

---

## 4. Regular Expressions, NFA and DFA

### Use in system software

Regular expressions are used in lexical analysis to describe tokens.

### Core ideas

1. RE describes a regular language.
2. Every RE can be converted to NFA.
3. Every NFA has an equivalent DFA.
4. DFA is preferred in scanners because it has deterministic moves.

### Standard construction flow

```text
Regular Expression -> NFA -> DFA -> Minimized DFA
```

### Common exam point

For strings ending with `abb`:

```text
(a|b)*abb
```

---

## 5. Top Down Parsing

### Definition

Top down parsing constructs the parse tree from the start symbol towards the terminals.

### Types

1. Recursive descent parsing
2. Recursive descent with backtracking
3. Predictive parsing

### Recursive descent with backtracking

1. One procedure for each non-terminal.
2. Try productions one by one.
3. If a choice fails, go back and try another production.
4. Simple, but inefficient.

### Predictive parsing

1. Non-recursive or recursive top-down method.
2. Uses look-ahead symbol.
3. No backtracking needed.
4. Requires LL(1) grammar.

---

## 6. Left Recursion and Left Factoring

### Left recursion

Grammar is left recursive if:

```text
A -> A alpha | beta
```

### Removal formula

```text
A  -> beta A'
A' -> alpha A' | epsilon
```

### Left factoring

Used when productions have common prefix.

If:

```text
A -> alpha beta1 | alpha beta2
```

Then:

```text
A  -> alpha A'
A' -> beta1 | beta2
```

### Why needed

Both are important to convert grammar into predictive parser form.

---

## 7. FIRST and FOLLOW

### FIRST

`FIRST(alpha)` = set of terminals that can appear first in strings derived from `alpha`.

### FOLLOW

`FOLLOW(A)` = set of terminals that can appear immediately to the right of `A` in some sentential form.

### Rules for FIRST

1. If `X` is a terminal, `FIRST(X) = {X}`.
2. If `A -> epsilon`, then `epsilon` is in `FIRST(A)`.
3. If `A -> X1 X2 ... Xn`, add `FIRST(X1)` excluding epsilon.
4. If `X1` can derive epsilon, continue with `X2`, and so on.

### Rules for FOLLOW

1. Put `$` in FOLLOW of start symbol.
2. If `A -> alpha B beta`, add `FIRST(beta)` excluding epsilon to `FOLLOW(B)`.
3. If `beta` can derive epsilon, add `FOLLOW(A)` to `FOLLOW(B)`.

### Most important use

FIRST and FOLLOW are used to construct LL(1) parsing tables.

---

## 8. LL(1) Parsing

### Meaning of LL(1)

1. First `L`: scan input from Left to right.
2. Second `L`: produce Leftmost derivation.
3. `1`: use one symbol of look-ahead.

### Conditions for LL(1)

For a non-terminal `A` with productions `A -> alpha | beta`:

1. `FIRST(alpha)` and `FIRST(beta)` must be disjoint.
2. If epsilon is in one FIRST set, then the other FIRST set must be disjoint from `FOLLOW(A)`.
3. Grammar should be free from left recursion and ambiguity for practical predictive parsing.

### Parse table rule

For `A -> alpha`:

1. Put it in `M[A, a]` for every `a` in `FIRST(alpha)` excluding epsilon.
2. If epsilon is in `FIRST(alpha)`, put it in `M[A, b]` for every `b` in `FOLLOW(A)`.

### Acceptance rule

String is accepted if both stack and input become `$` at the same time.

### Common expression grammar in LL(1) form

```text
E  -> T E'
E' -> + T E' | epsilon
T  -> F T'
T' -> * F T' | epsilon
F  -> id | (E)
```

### Why this grammar is popular

1. `*` gets higher precedence than `+`.
2. Associativity is naturally handled.
3. It is suitable for predictive parsing.

---

## 9. Bottom Up Parsing

### Definition

Bottom up parsing constructs the parse tree from leaves to root. It reduces the input string to the start symbol.

### Key term: handle

A handle is a substring that matches the RHS of a production and whose reduction represents one step of reverse rightmost derivation.

### Handle pruning

Repeatedly find handle and reduce it until the start symbol is obtained.

### Shift-reduce parser actions

1. Shift
2. Reduce
3. Accept
4. Error

### Example grammar often asked

```text
S -> SS+ | SS* | a
```

Language generated:

```text
Postfix expressions using operand a and operators +, *
```

---

## 10. LR Parsing Concepts

### Expansion of LR

1. `L` = scan input Left to right.
2. `R` = construct Rightmost derivation in reverse.

### Main types

1. LR(0)
2. SLR(1)
3. Canonical LR(1)
4. LALR(1)

### LR(0) item

An LR item is a production with a dot showing parser progress.

Example:

```text
E -> E . + T
```

### Important functions

1. `closure(I)`
2. `goto(I, X)`

### Typical exam question

For grammar:

```text
S -> L = R | R
L -> *R | id
R -> L
```

Main conclusion:

```text
Grammar is not LR(0) because of shift/reduce conflict.
```

Reason:

State containing both:

```text
S -> L . = R
R -> L .
```

causes conflict on symbol `=`.

---

## 11. Macro Processor

### Macro

A macro is a named sequence of assembly statements that can be expanded when invoked.

### Advantage

Reduces repetitive coding and improves program readability.

### Important terms

1. MNT = Macro Name Table
2. MDT = Macro Definition Table
3. PNTAB = Parameter Name Table
4. ALA = Argument List Array

### Parameter types

1. Positional parameters
2. Keyword parameters
3. Default parameters

### Keyword parameter example

```text
MACRO
LOAD &ARG, &REG=AREG
MOVER &REG, &ARG
MEND
```

### Expansion time variables

Variables used during expansion only, for example loop counts or generated labels.

### Conditional assembly

Use `AIF`, `AGO` to select statements during expansion.

### Generation time activities

These are operations performed during expansion, not during execution of the final machine program.

---

## 12. Assembler

### Definition

Assembler converts assembly language program into machine code.

### Why two-pass assembler is used

Because of forward references.

Example:

```text
JMP LOOP
...
LOOP: ADD B
```

At first occurrence of `LOOP`, its address is not yet known.

### Pass I

1. Assign addresses using location counter.
2. Build SYMTAB.
3. Enter literals in LITTAB.
4. Build POOLTAB.
5. Produce intermediate code.

### Pass II

1. Use SYMTAB and LITTAB.
2. Replace symbols and literals by addresses.
3. Generate target code.

### Main tables

1. OPTAB = opcode information
2. SYMTAB = symbols and addresses
3. LITTAB = literals and addresses
4. POOLTAB = starting index of each literal pool

### Important directives

1. `START` = initialize LC
2. `END` = end of source program
3. `ORIGIN` = change LC
4. `EQU` = assign symbol value
5. `LTORG` = place literals at current location
6. `DS` = reserve storage
7. `DC` = define constant

### One-line distinctions

1. `EQU` gives one symbol the value of another expression.
2. `ORIGIN` changes LC.
3. `LTORG` assigns addresses to pending literals.

---

## 13. Intermediate Code and Target Code

### Intermediate code notation often used in exams

1. `IS` = Imperative statement
2. `AD` = Assembler directive
3. `DL` = Declarative statement

### Example

```text
MOVER AREG, =5
```

may be written as:

```text
(IS,04) (1) (L,1)
```

### Why intermediate code is useful

1. Keeps Pass I and Pass II separate.
2. Helps resolve forward references.
3. Makes code generation systematic.

---

## 14. Linker and Loader

### Linker

1. Combines object modules.
2. Resolves external symbol references.
3. Performs relocation if required.

### Loader

1. Allocates memory.
2. Loads object code into memory.
3. Performs final relocation.
4. Transfers control to starting address.

### Types often asked

1. Absolute loader
2. Relocating loader
3. Linking loader / direct linking loader
4. Dynamic linking loader

---

## 15. Relocation and Modification Records

### Relocation

Relocation means adjusting address-dependent parts of the program when it is loaded at a memory location different from the assumed address.

### Relocation bits

Extra bits associated with object code words indicating whether relocation is required.

### Modification record

Record specifying which address field must be modified, its length, and sometimes the related external symbol.

### Key difference

1. Relocation bits are compact and simple.
2. Modification records are more flexible, especially for external references.

---

## 16. One-Pass Module Assembler and External Symbols

### Branch to external symbol

When external symbol address is unknown during assembly:

1. Enter symbol in external reference table.
2. Put temporary address in object code.
3. Generate relocation / modification information.
4. Let linker-loader resolve it later.

This is the standard answer for external forward branch handling.

---

## 17. Symbol Table Organization

### Common methods

1. Linear list
2. Ordered list / array
3. Binary search tree
4. Hash table

### Best practical answer

Hash table is preferred in real compilers because average insertion and search are both fast.

---

## 18. High-Yield Definitions

### Token

A class of lexemes recognized by the lexical analyser.

### Lexeme

Actual character sequence matched for a token.

### Pattern

Rule describing the form of a token.

### Handle

Substring matching RHS of a production and reduced during bottom-up parsing.

### Ambiguous grammar

A grammar is ambiguous if a string has more than one parse tree or more than one leftmost/rightmost derivation.

### LL(1) grammar

Grammar that can be parsed left to right, constructing leftmost derivation, using one look-ahead symbol.

### LR grammar

Grammar that can be parsed left to right while constructing rightmost derivation in reverse.

---

## 19. Most Repeated Exam Results

### Expression grammar after removing left recursion

```text
E  -> T E'
E' -> + T E' | epsilon
T  -> F T'
T' -> * F T' | epsilon
F  -> id | (E)
```

### Boolean expression grammar in LL(1) form

```text
E  -> T E'
E' -> or T E' | epsilon
T  -> F T'
T' -> and F T' | epsilon
F  -> not F | (E) | true | false
```

### Postfix expression grammar

```text
S -> SS+ | SS* | a
```

Language:

```text
Postfix expressions over operand a using + and *
```

### Assignment grammar often asked in LR

```text
S -> L = R | R
L -> *R | id
R -> L
```

Result:

```text
Not LR(0)
```

---

## 20. Last-Minute Exam Strategy

1. For theory answers, start with one-line definition.
2. Then write 3-4 clear points.
3. Add one small example if possible.
4. For parsing questions, always show FIRST/FOLLOW before table.
5. For LR questions, number productions first.
6. For assembler questions, make LC table first, then SYMTAB/LITTAB/POOLTAB, then IC.
7. If grammar is not LL(1) or not LR(0), explicitly state the conflict and the reason.

---

## 21. Ultra-Short Revision Lines

1. Lexical analyser forms tokens.
2. Parser checks grammar.
3. FIRST tells what can start.
4. FOLLOW tells what can come next.
5. LL(1) needs no backtracking.
6. Bottom-up parsing uses handle pruning.
7. LR item = production with dot.
8. Two-pass assembler is used for forward references.
9. SYMTAB stores symbols, LITTAB stores literals, POOLTAB stores literal-pool starts.
10. Linker resolves external references, loader places code in memory.

---

## 22. Final Memory Box

```text
Token / Lexeme / Pattern
FIRST / FOLLOW / Parse Table
Left Recursion / Left Factoring
LL(1) / Top Down / Predictive Parser
Bottom Up / Handle / Shift-Reduce
LR(0) / SLR / LR(1)
Macro / MNT / MDT / ALA
Assembler / SYMTAB / LITTAB / POOLTAB
ORIGIN / EQU / LTORG / START / END
Relocation / Modification Record
Linker / Loader / External Symbol
```

If these terms are clear, most mid-semester System Software questions become manageable.
