# System Software Lab 3

---

## Question 1: Recursive Descent Parser (RDP) without Backtracking

`1. Implement RDP without backtracking for the given grammar.`

**File:** `RDP.c`

### Problem Statement

Implement a Recursive Descent Parser without backtracking for the following grammar:

| Non-Terminal | Production |
|--------------|------------|
| E | E + T \| T |
| T | T * F \| F |
| F | ( E ) \| id |

**Grammar Definition**

```
E  → E + T | T
T  → T * F | F
F  → ( E ) | id
```

This grammar represents arithmetic expressions with `+` and `*` operators, parentheses, and identifiers.

### Concept Understanding

**What is Parsing?**

Parsing is the second phase of a compiler (after lexical analysis). It checks if the sequence of tokens follows the grammar rules of the language. Think of it as checking if a sentence follows proper grammar.

```
Lexical Analysis: "a + b * c" → tokens: [id, +, id, *, id]
Parsing: Checks if tokens follow: E → E + T | T, etc.
```

**What is a Recursive Descent Parser?**

A **top-down** parsing technique where:
- We have one function for each non-terminal in the grammar
- Each function recursively calls other functions based on grammar rules
- We start from the start symbol (E) and try to derive the input string

```
For grammar: E → T E'
             E' → + T E' | ε

We create functions:
- void E()   → calls T(), then E_prime()
- void E_prime() → if see '+', consume it, call T(), E_prime()
```

**Why "Without Backtracking"?**

Backtracking means going back and trying another alternative if current choice fails. It's slow and complex.

**Without backtracking** means:
- We make the correct choice by looking at the next input symbol (lookahead)
- No going back - if we choose wrong, it's an error
- This requires the grammar to be **LL(1)** - we can decide which production to use by looking at just 1 symbol ahead

**The Problem: Left Recursion**

The given grammar has **left recursion**:
```
E → E + T | T
```

Here `E` calls itself as the **first** thing (leftmost). If we write:
```c
void E() {
    E();  // Infinite loop! Never terminates
    match('+');
    T();
}
```

This causes infinite recursion because `E()` keeps calling `E()` forever.

**The Solution: Eliminate Left Recursion**

General rule to eliminate left recursion:
```
A → Aα | β
```
Becomes:
```
A  → β A'
A' → α A' | ε
```

Applying to our grammar:

**Original:**
```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

**After elimination:**
```
E  → T E'
E' → + T E' | ε

T  → F T'
T' → * F T' | ε

F  → ( E ) | id
```

Now there's no left recursion. Each function makes progress by consuming input or calling a different function first.

**What is ε (epsilon)?**

Epsilon means "empty" or "nothing". Production `E' → ε` means E' can produce nothing.

In code, we simply do nothing (return without consuming input):
```c
void E_prime() {
    if (input[pos] == '+') {
        pos++;  // consume '+'
        T();
        E_prime();
    }
    // else: epsilon - just return, do nothing
}
```

**Understanding the Grammar**

Let's trace `a + b * c`:

```
E
└── T
│   └── F
│       └── id (a)
└── E'
    └── + T
    │   └── F
    │       └── id (b)
    │   └── T'
    │       └── * F
    │           └── id (c)
    │       └── T'
    │           └── ε
    └── E'
        └── ε
```

The grammar enforces **operator precedence**:
- `*` binds tighter than `+` because `*` is handled in T/T' (inner level)
- `+` is handled in E/E' (outer level)
- So `a + b * c` is parsed as `a + (b * c)`, not `(a + b) * c`

### Code Understanding

**File Structure:**
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

char input[100];   // Input string
int pos = 0;       // Current position in input
int error = 0;     // Error flag

// Function declarations (needed because of mutual recursion)
void E();
void E_prime();
void T();
void T_prime();
void F();
```

**Helper Functions:**

```c
// Skip whitespace in input
void skip_space() {
    while (input[pos] == ' ' || input[pos] == '\t')
        pos++;
}

// Match expected character, set error if mismatch
void match(char c) {
    skip_space();
    if (input[pos] == c)
        pos++;
    else
        error = 1;
}
```

**Grammar Functions:**

```c
// E → T E'
void E() {
    if (error) return;  // Stop if error already occurred
    T();                // First call T
    E_prime();          // Then call E'
}

// E' → + T E' | ε
void E_prime() {
    if (error) return;
    skip_space();
    if (input[pos] == '+') {    // If we see '+', take first alternative
        pos++;                   // Consume '+'
        T();                     // Call T
        E_prime();               // Recursive call for more additions
    }
    // else: epsilon (ε) - do nothing, just return
}
```

```c
// T → F T'
void T() {
    if (error) return;
    F();                // First call F
    T_prime();          // Then call T'
}

// T' → * F T' | ε
void T_prime() {
    if (error) return;
    skip_space();
    if (input[pos] == '*') {    // If we see '*', take first alternative
        pos++;                   // Consume '*'
        F();                     // Call F
        T_prime();               // Recursive call for more multiplications
    }
    // else: epsilon - do nothing
}
```

```c
// F → ( E ) | id
void F() {
    if (error) return;
    skip_space();
    
    if (input[pos] == '(') {    // Alternative 1: ( E )
        pos++;                   // Consume '('
        E();                     // Parse expression inside
        match(')');              // Expect and consume ')'
    }
    else if (isalpha(input[pos])) {  // Alternative 2: identifier
        while (isalnum(input[pos]))   // Consume entire identifier
            pos++;
    }
    else if (isdigit(input[pos])) {  // Also accept numbers
        while (isdigit(input[pos]))
            pos++;
    }
    else {
        error = 1;  // Neither ( nor id - error!
    }
}
```

**Main Function:**

```c
int main() {
    printf("Enter expression: ");
    fgets(input, sizeof(input), stdin);
    input[strlen(input)-1] = '\0';  // Remove newline
    
    // Display the transformed grammar
    printf("\nGrammar (after left recursion elimination):\n");
    printf("E  -> T E'\n");
    printf("E' -> + T E' | epsilon\n");
    printf("T  -> F T'\n");
    printf("T' -> * F T' | epsilon\n");
    printf("F  -> ( E ) | id\n\n");
    
    E();           // Start parsing from E
    skip_space();  // Skip trailing whitespace
    
    // Check if entire input was consumed without errors
    if (!error && input[pos] == '\0')
        printf("VALID expression (Accepted)\n");
    else
        printf("INVALID expression (Rejected)\n");
    
    return 0;
}
```

**Algorithm Flow:**

```
1. Read input expression
2. Start with E() - the start symbol
3. Each function:
   - Looks at current input character (lookahead)
   - Decides which production to use
   - Consumes input and/or calls other functions
4. After E() returns:
   - If no error AND entire input consumed → VALID
   - Otherwise → INVALID
```

**Trace Example: `a + b`**

```
Initial: input = "a + b", pos = 0

E() called
├── T() called
│   ├── F() called
│   │   └── sees 'a' (letter), consumes "a", pos = 1
│   └── T_prime() called
│       └── sees ' ' then '+', not '*', returns (epsilon)
└── E_prime() called
    ├── sees '+', consumes it, pos = 3
    ├── T() called
    │   ├── F() called
    │   │   └── sees 'b', consumes it, pos = 5
    │   └── T_prime() called
    │       └── sees '\0', returns (epsilon)
    └── E_prime() called
        └── sees '\0', returns (epsilon)

Final: pos = 5, input[5] = '\0', error = 0
Result: VALID
```

**Trace Example: `a + + b` (Invalid)**

```
E() → T() → F() consumes 'a'
    → T_prime() returns (no '*')
→ E_prime() sees '+', consumes it
    → T() → F() sees '+' → NOT a letter, digit, or '('
            → error = 1

Result: INVALID (consecutive operators)
```

### Viva Prep

**Q: What is a Recursive Descent Parser?**
A: A top-down parser where each non-terminal in the grammar is implemented as a function. Functions call each other recursively to parse the input according to grammar rules.

**Q: Why can't we use left-recursive grammar directly in RDP?**
A: Left recursion like `E → E + T` causes infinite recursion. The function E() would call E() as its first action, never consuming any input, leading to infinite loop and stack overflow.

**Q: How do you eliminate left recursion?**
A: Convert `A → Aα | β` to:
- `A → β A'`
- `A' → α A' | ε`

For `E → E + T | T`:
- `E → T E'`
- `E' → + T E' | ε`

**Q: What is ε (epsilon) in grammar?**
A: Epsilon represents empty string - producing nothing. In code, we implement it by simply returning from the function without consuming any input.

**Q: What is lookahead?**
A: Looking at the next input symbol(s) without consuming them, to decide which production rule to apply. In our parser, we look at `input[pos]` to decide.

**Q: What makes a grammar LL(1)?**
A: **L**eft-to-right scan, **L**eftmost derivation, **1** symbol lookahead. The grammar allows us to decide which production to use by looking at just one symbol ahead. No backtracking needed.

**Q: What is the difference between top-down and bottom-up parsing?**
A: 
- **Top-down:** Start from start symbol, try to derive input. (RDP, LL parsers)
- **Bottom-up:** Start from input, try to reduce to start symbol. (LR parsers, shift-reduce)

**Q: Why do we need `skip_space()` function?**
A: To handle whitespace in input. Without it, "a + b" would fail because after 'a', we'd see ' ' instead of '+'. We skip spaces before checking input.

**Q: How does operator precedence work in this grammar?**
A: Higher precedence operators are handled at lower levels (closer to terminals). `*` is in T/T' (lower level), `+` is in E/E' (higher level). So `*` binds tighter than `+`.

**Q: What is the role of the `error` flag?**
A: Once an error is detected, we set `error = 1`. All functions check this flag first and return immediately if set. This prevents cascading error messages and ensures we report the first error.

**Q: What would happen if we don't check `input[pos] == '\0'` at the end?**
A: We might accept invalid input. For example, "a b" would be accepted because "a" is valid and E() returns successfully. But we haven't consumed "b". Checking for end-of-input ensures the entire expression was parsed.

**Q: How would you add `-` (subtraction) operator to this grammar?**
A: Modify E_prime to also check for `-`:
```c
void E_prime() {
    if (input[pos] == '+' || input[pos] == '-') {
        pos++;
        T();
        E_prime();
    }
}
```

**Q: What is a predictive parser?**
A: A recursive descent parser that doesn't require backtracking. It can always predict which production to use based on lookahead. Also called LL(1) parser.

**Q: What is the difference between RDP and other parsers (like LR)?**
A: 
- RDP: Simple to implement, requires LL(1) grammar, limited power
- LR parsers: More complex, handle larger class of grammars, used in real compilers (yacc/bison)

---

## Quick Reference

### How to Compile and Run

```bash
# Compile
gcc RDP.c -o rdp

# Run
./rdp
```

### Sample Test Cases

| Input | Expected Output |
|-------|-----------------|
| `a + b` | VALID |
| `a * b + c` | VALID |
| `(a + b) * c` | VALID |
| `a + b * c` | VALID |
| `((a))` | VALID |
| `a +` | INVALID |
| `+ a` | INVALID |
| `a + + b` | INVALID |
| `(a + b` | INVALID |
| `a b` | INVALID |

### Grammar Transformation Summary

**Original (with left recursion):**
```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

**Transformed (without left recursion):**
```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

### Files in Lab3/

| File | Purpose |
|------|---------|
| `RDP.c` | Recursive Descent Parser implementation |
| `Questions.md` | Lab question/problem statement |
| `README.md` | This documentation file |

### Key Concepts Summary

| Concept | Description |
|---------|-------------|
| Parsing | Checking if tokens follow grammar rules |
| Top-down parsing | Start from start symbol, derive input |
| Left recursion | `A → Aα`, causes infinite loop in RDP |
| Epsilon (ε) | Empty production, produces nothing |
| Lookahead | Peeking at next symbol to decide production |
| LL(1) | Left-to-right, Leftmost derivation, 1 lookahead |
| Predictive parser | RDP without backtracking |
