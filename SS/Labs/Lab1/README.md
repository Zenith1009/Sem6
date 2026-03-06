# System Software Lab 1

## Overview
This lab focuses on fundamental concepts in compiler design and automata theory, specifically covering regular expressions, lexical analysis, and pattern recognition.

---

## Problem 1: Regular Expression to DFA Conversion

### Problem Statement
Write a program to convert a Regular Expression to a DFA (Deterministic Finite Automaton).

### Concept
- **Regular Expression**: Patterns like `ab*`, `a+b`, `a*b+` using only concatenation, `*` (zero or more), and `+` (one or more)
- **DFA**: One transition per input symbol from every state; no epsilon moves
- **This implementation**: Builds a compact DFA directly from the regex (supports concatenation, `*`, `+`; does **not** support `|` alternation)

### How the Program Works
1. Scan the regex left to right.
2. For each literal:
   - If followed by `*`: add a self-loop on the current state.
   - If followed by `+`: add a mandatory step, then a self-loop.
   - Otherwise: add a simple transition to the next state.
3. Track `q0` as start and the last state as final.
4. Validate input strings by walking the deterministic transitions.

### Sample Input/Output
```
Input regex: ab*
DFA transitions:
q0 --a--> q1
q1 --b--> q1   (loop)
Start: q0
Final: q1

Tests:
a    -> ACCEPTED
ab   -> ACCEPTED
abb  -> ACCEPTED
b    -> REJECTED
```

### Viva Questions
1. **What is the difference between NFA and DFA?**
   - NFA can have multiple transitions for the same input; DFA has exactly one.
   - NFA may have epsilon transitions; DFA cannot.
   - Every NFA has an equivalent DFA (subset construction).

2. **What is subset construction?**
   - Converts an NFA (with or without ε) into an equivalent DFA by treating sets of NFA states as single DFA states.

3. **Advantages of DFA over NFA?**
   - Deterministic and fast (no backtracking), simpler to implement.

4. **Why convert regex to DFA?**
   - Direct pattern matching for lexical analyzers and text tools.
   - Guarantees linear-time recognition.

---

## Problem 2: Lexical Analyzer (Tokenizer)

### Problem Statement
Write a program to detect and classify tokens in a C program statement.

### Concept
- **Lexical Analysis**: First phase of compilation
- **Token**: Smallest meaningful unit in source code
- **Token Types**: Keywords, Identifiers, Numbers, Operators, Special Symbols

### Token Categories

| Type | Description | Examples |
|------|-------------|----------|
| Keyword | Reserved words | int, if, while, for |
| Identifier | Variable/function names | count, sum, myVar |
| Number | Numeric literals | 123, 456 |
| Operator | Arithmetic/logical operators | +, -, *, /, = |
| Special Symbol | Punctuation | ;, (, ), {, } |

### How the Program Works
1. Reads a C statement character by character
2. Groups characters into meaningful tokens
3. Classifies each token by type
4. Outputs the token type and value

### Sample Input/Output
```
Input: int sum = 10 + 20;
Output:
Keyword: int
Identifier: sum
Operator: =
Number: 10
Operator: +
Number: 20
Special Symbol: ;
```

### Viva Questions
1. **What is lexical analysis?**
   - First phase of compiler
   - Converts source code into tokens
   - Removes whitespace and comments

2. **What is a token?**
   - Smallest unit of meaning in source code
   - Has a type and value
   - Examples: keywords, identifiers, literals

3. **What is a lexeme?**
   - Actual string/sequence that forms a token
   - Example: In "int x", "int" is lexeme of token KEYWORD

4. **Difference between keyword and identifier?**
   - Keywords are reserved by language (int, if, while)
   - Identifiers are user-defined names (myVar, count)

5. **What is symbol table?**
   - Data structure storing identifier information
   - Contains name, type, scope, memory location
   - Updated during lexical and syntax analysis

6. **Role of lexical analyzer?**
   - Tokenization of source code
   - Error detection (invalid characters)
   - Communication with parser

---

## Problem 3: String Pattern Recognition

### Problem Statement
Write a program to recognize strings matching patterns `b+a*` and `a*b+a*`.

### Concept
- **Pattern Matching**: Checking if string follows specific pattern
- **Finite Automata**: Used to recognize patterns
- **State Transitions**: Moving between states based on input

### Pattern Explanations

#### Pattern 1: `b+a*`
- **Meaning**: One or more 'b's followed by zero or more 'a's
- **Valid**: b, ba, baa, bb, bba, bbaa
- **Invalid**: a, ab, aba, empty string

#### Pattern 2: `a*b+a*`
- **Meaning**: Zero or more 'a's, then one or more 'b's, then zero or more 'a's
- **Valid**: b, ba, ab, aba, aabba, baa
- **Invalid**: a, aa, empty string

### Algorithm
1. Use state machine approach
2. Check each character sequentially
3. Count required characters (b+ means at least one b)
4. Verify entire string is consumed

### Sample Input/Output
```
Input: bba
Output:
Pattern 'b+a*': ACCEPTED
Pattern 'a*b+a*': ACCEPTED

Input: aaa
Output:
Pattern 'b+a*': REJECTED
Pattern 'a*b+a*': REJECTED
```

### Viva Questions
1. **What is pattern recognition?**
   - Process of matching strings against patterns
   - Used in text processing, validation
   - Based on formal language theory

2. **What does b+ mean?**
   - One or more occurrences of 'b'
   - Must have at least one 'b'
   - Can have multiple consecutive 'b's

3. **What does a* mean?**
   - Zero or more occurrences of 'a'
   - String can have no 'a' at all
   - String can have any number of 'a's

4. **How is this related to DFA/NFA?**
   - Each pattern can be represented as finite automaton
   - Program simulates state transitions
   - Acceptance happens when final state reached

5. **Real-world applications?**
   - Email validation (pattern matching)
   - Phone number validation
   - Syntax checking in compilers
   - Search engines and text editors

---

## Compilation and Execution

### Compiling the Programs
```bash
gcc 1_regex_to_dfa.c -o regex_dfa
gcc 2_lexical_analyzer.c -o lexer
gcc 3_string_recognizer.c -o recognizer
```

### Running the Programs
```bash
./regex_dfa
./lexer
./recognizer
```

---

## Important Concepts for Viva

### 1. Compiler Phases
1. **Lexical Analysis** - Tokenization
2. **Syntax Analysis** - Parsing
3. **Semantic Analysis** - Type checking
4. **Intermediate Code Generation**
5. **Code Optimization**
6. **Code Generation**

### 2. Finite Automata Types
- **DFA (Deterministic)**: One transition per input
- **NFA (Non-deterministic)**: Multiple transitions possible
- **ε-NFA**: NFA with epsilon transitions

### 3. Regular Expression Operators
- `*` (Kleene star): 0 or more
- `+` (Plus): 1 or more
- `?` (Optional): 0 or 1
- `|` (Union): Or
- `.` (Concatenation): And then

### 4. Lexical Analysis Terms
- **Lexeme**: Actual character sequence
- **Token**: Classification + Value
- **Pattern**: Rule for recognizing lexemes
- **Symbol Table**: Storage for identifiers

---

## Additional Practice Questions

1. Draw NFA for regex `(a|b)*abb`
2. Convert NFA to DFA using subset construction
3. Write regex for: "strings ending with 01"
4. Implement lexer for recognizing floating-point numbers
5. Design DFA accepting strings with even number of 0's
6. What is the pumping lemma for regular languages?
7. Difference between parser and lexer?
8. What are ambiguous grammars?

---

## Tips for Lab Exam
1. Understand state transitions clearly
2. Practice drawing automata diagrams
3. Know regex operators by heart
4. Remember token classification rules
5. Be able to trace program execution step-by-step
6. Understand difference between NFA and DFA
7. Practice converting between regex, NFA, and DFA

---
---

# Lab 1 Examples

---

## 1) Regex to DFA (`1_regex_to_dfa.c`)
Supports concatenation, `*` (zero or more), `+` (one or more). No alternation `|`.

### Example A: `ab*`
```
$ ./regex_dfa
Regex to DFA (supports *, +, concat)
Enter regex: ab*

DFA
State    Input    Next
------------------------
q0       a        q1
q1       b        q1
------------------------
Start: q0
Final: q1

Test a string? (y/n): y
String: a
ACCEPTED

Test a string? (y/n): y
String: ab
ACCEPTED

Test a string? (y/n): y
String: abb
ACCEPTED

Test a string? (y/n): y
String: b
REJECTED

Test a string? (y/n): n
```

### Example B: `a+b`
```
Enter regex: a+b

DFA
q0 --a--> q1
q1 --a--> q1 (loop)
q1 --b--> q2
Start: q0, Final: q2

Strings:
- ab    -> ACCEPTED
- aab   -> ACCEPTED
- aaab  -> ACCEPTED
- b     -> REJECTED
- a     -> REJECTED
```

### Example C: `a*b+`
```
Enter regex: a*b+

DFA (key transitions):
q0 --a--> q0 (loop)
q0 --b--> q1
q1 --b--> q1 (loop)
Start: q0, Final: q1

Strings:
- b      -> ACCEPTED
- ab     -> ACCEPTED
- aab    -> ACCEPTED
- abb    -> ACCEPTED
- aa     -> REJECTED
- a      -> REJECTED
```

---

## 2) Lexical Analyzer (`2_lexical_analyzer.c`)
Reads one C statement and classifies tokens.

```
$ ./lexer
Enter a C statement: int sum = 10 + 20;

Tokens identified:
-------------------
Keyword: int
Identifier: sum
Operator: =
Number: 10
Operator: +
Number: 20
Special Symbol: ;
```

Enter a C statemt: if (num > 50) {printf("Start the show");}

---

## 3) String Recognizer (`3_string_recognizer.c`)
Checks patterns `b+a*` and `a*b+a*`.

### Example A
```
$ ./recognizer
Enter a string: bba

Pattern Recognition Results:
-----------------------------
Pattern 'b+a*': ACCEPTED
Pattern 'a*b+a*': ACCEPTED
```

### Example B
```
Enter a string: aaa

Pattern Recognition Results:
-----------------------------
Pattern 'b+a*': REJECTED
Pattern 'a*b+a*': REJECTED
```

### Example C
```
Enter a string: abba

Pattern Recognition Results:
-----------------------------
Pattern 'b+a*': REJECTED
Pattern 'a*b+a*': ACCEPTED
```
