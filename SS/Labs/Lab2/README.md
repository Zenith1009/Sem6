# System Software Lab 2

---

## Question 1: Arithmetic Expression Analyzer 
`1. Write a C Program to recognize a valid arithmetic expression and identify the identifiers and operators present. Print them separately.`

**File:** `1_arithmetic_expression.c`

### Problem Statement

Write a C Program to recognize a valid arithmetic expression and identify the identifiers and operators present. Print them separately.

### Concept Understanding

**What is Lexical Analysis?**

Lexical analysis is the first phase of a compiler. It reads the source code character by character and groups them into meaningful units called **tokens**. Think of it like reading a sentence and identifying words, punctuation, etc.

For example, in `a + b * 2`:
- `a`, `b` are **identifiers** (variable names)
- `+`, `*` are **operators**
- `2` is a **numeric literal**

**What is an Identifier?**

An identifier is a name we give to variables, functions, etc. Rules:
- Must start with a letter (a-z, A-Z) or underscore (_)
- Can contain letters, digits (0-9), and underscores
- Cannot be a keyword

Valid: `x`, `count`, `_temp`, `var1`
Invalid: `1var`, `my-var`, `int`

**What are Operators?**

Operators perform operations on operands. Arithmetic operators:
| Operator | Meaning |
|----------|---------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `%` | Modulo (remainder) |

### Code Understanding

```
How the program works:

1. Read expression from user using fgets()

2. Loop through each character:
   - If space → skip
   - If operator (+,-,*,/,%) → store in operators array
   - If letter → it's start of identifier, keep reading until non-alphanumeric
   - If digit → it's a number, skip it
   - If parenthesis → skip
   - Anything else → invalid

3. Print results
```

**Key variables:**
- `identifiers[20][20]` - 2D array to store identifier names
- `operators[20]` - array to store operator characters
- `id_count`, `op_count` - counters

**Key logic:**
```c
// Check for identifier (starts with letter)
if (isalpha(expr[i])) {
    j = 0;
    while (isalnum(expr[i])) {  // keep reading letters/digits
        token[j] = expr[i];
        j++; i++;
    }
    token[j] = '\0';
    strcpy(identifiers[id_count], token);
    id_count++;
}
```

### Viva Prep

**Q: What is a lexical analyzer?**
A: First phase of compiler that reads source code and converts it into tokens. Also called scanner or tokenizer.

**Q: What is a token?**
A: A meaningful unit in source code. Types: identifiers, keywords, operators, literals, punctuation.

**Q: How do you identify an identifier?**
A: Check if it starts with letter/underscore, then continue while alphanumeric. Use `isalpha()` and `isalnum()` functions.

**Q: What is the difference between lexical analysis and parsing?**
A: Lexical analysis breaks code into tokens. Parsing checks if tokens follow grammar rules (syntax analysis).

**Q: Why use `isalpha()` and `isalnum()`?**
A: `isalpha(c)` returns true if c is a letter. `isalnum(c)` returns true if c is letter or digit. Defined in `<ctype.h>`.

---

## Question 2: Comment Identifier
`2. Write a C program to identify whether a given line is a comment or not.`

**File:** `2_comment_identifier.c`

### Problem Statement

Write a C program to identify whether a given line is a comment or not.

### Concept Understanding

**What are Comments?**

Comments are text in source code that the compiler ignores. Used for documentation and explanation.

**Types of Comments in C:**

1. **Single-line comment:** `// comment here`
   - Starts with `//`
   - Extends to end of line
   
2. **Multi-line comment:** `/* comment here */`
   - Starts with `/*`
   - Ends with `*/`
   - Can span multiple lines

**Why identify comments?**

During compilation, the preprocessor removes all comments before actual compilation. This is part of lexical analysis phase.

**Comment Examples:**
```c
// This is single-line comment

/* This is 
   multi-line
   comment */

int x = 5;  // inline comment

/* Single line but multi-line style */
```

### Code Understanding

```
How the program works:

1. Read a line using fgets()

2. Skip leading whitespace (spaces, tabs)
   - Use index i to track position
   - while (line[i] == ' ' || line[i] == '\t') i++

3. Check what the line starts with:
   - If starts with "//" → single-line comment
   - If starts with "/*":
     - If also has "*/" → complete multi-line comment
     - Else → multi-line comment START
   - If has "*/" anywhere → multi-line comment END
   - Otherwise → not a comment
```

**Key logic:**
```c
// Check for single-line comment
if (line[i] == '/' && line[i+1] == '/') {
     printf("Single-line comment\n");
}
// Check for multi-line start
else if (line[i] == '/' && line[i+1] == '*') {
     if (strstr(line, "*/") != NULL)  // also ends on same line
        printf("Complete multi-line comment\n");
    else
        printf("Multi-line comment START\n");
}
```

**Why skip leading whitespace?**
Because `   // comment` should still be detected as comment, even with spaces before it.

### Viva Prep

**Q: What are comments used for?**
A: Documentation, explaining code logic, temporarily disabling code, making code readable.

**Q: Which phase of compiler handles comments?**
A: Preprocessing phase (before lexical analysis) or during lexical analysis. Comments are replaced with single space.

**Q: Can we nest multi-line comments in C?**
A: No. `/* outer /* inner */ */` will cause error. The first `*/` ends the comment.

**Q: What is `strstr()` function?**
A: `strstr(str, substr)` finds first occurrence of substr in str. Returns pointer to match or NULL if not found. Defined in `<string.h>`.

**Q: Difference between `//` and `/* */`?**
A: `//` is C99 onwards, single line only. `/* */` is original C style, can span multiple lines.

---

## Question 3: Two-Pass 8085 Assembler

`3. Create Assembler as discussed in Class.`

**Folder:** `assembler/`

### Problem Statement

Write a C Program to implement a Two-Pass Assembler for 8085 with:
- Static OPTAB (Operation Code Table) - contains opcode, format, length
- Pass 1: Validate opcodes and build SYMTAB (Symbol Table)
- Pass 2: Assemble instructions using SYMTAB

### Concept Understanding

**What is an Assembler?**

An assembler converts assembly language (human-readable mnemonics) into machine code (binary/hex that CPU understands).

```
Assembly:  MVI A, 05H    →    Assembler    →    Machine Code: 3E 05
```

**Why Two Passes?**

Because of **forward references**. Consider:
```asm
JMP LOOP      ; Using LOOP before it's defined!
...
LOOP: ADD B   ; LOOP is defined here
```

In one pass, when we see `JMP LOOP`, we don't know LOOP's address yet.

**Solution: Two passes**
- **Pass 1:** Just find all labels and their addresses. Build symbol table.
- **Pass 2:** Now we know all addresses. Generate actual machine code.

**Key Data Structures:**

1. **OPTAB (Operation Table)**
   - Hardcoded table of all valid mnemonics
   - Each entry: mnemonic, opcode, length, type
   ```c
   {"MVI", 0x00, 2, IK_MVI}   // MVI is 2 bytes
   {"HLT", 0x76, 1, IK_FIXED} // HLT is 1 byte
   ```

2. **SYMTAB (Symbol Table)**
   - Built during Pass 1
   - Maps label → address
   ```
   LOOP → 1003H
   END  → 100AH
   ```

3. **Location Counter (LC)**
   - Keeps track of current memory address
   - Starts at START address
   - Incremented by instruction length

**8085 Instruction Encoding:**

| Instruction | Format | Encoding |
|-------------|--------|----------|
| MVI r, data | 2 bytes | `00 DDD 110` + data byte |
| MOV r1, r2 | 1 byte | `01 DDD SSS` |
| ADD r | 1 byte | `10 000 SSS` |
| JMP addr | 3 bytes | `C3` + addr_low + addr_high |

**Register Codes (DDD/SSS):**
```
B=000, C=001, D=010, E=011, H=100, L=101, M=110, A=111
```

**Little-Endian Format:**
8085 stores addresses with low byte first.
`JMP 2000H` → `C3 00 20` (not C3 20 00)

### Code Understanding

**File Structure:**
- `assembler.h` - Data structures and declarations
- `Assembler.c` - Main program, OPTAB definition
- `Pass_1.c` - Pass 1 logic
- `Pass_2.c` - Pass 2 logic

**Pass 1 Algorithm:**
```
1. Open source file and intermediate file
2. Initialize LC = 0

3. For each line:
   a. Parse line into: label, opcode, operand
   b. If opcode is "START":
      - Set LC = operand value
   c. If label exists:
      - Add (label, LC) to SYMTAB
   d. Look up opcode in OPTAB
   e. If found: LC = LC + instruction_length
   f. Handle directives (BYTE, WORD, RESB, RESW)
   g. Write to intermediate file: LC, label, opcode, operand

4. Close files
```

**Pass 2 Algorithm:**
```
1. Open intermediate file and output file

2. For each line:
   a. Read: LC, label, opcode, operand
   b. Look up opcode in OPTAB
   c. Generate object code based on instruction type:
      - IK_FIXED: just the opcode byte
      - IK_MVI: opcode + register code + data byte
      - IK_JUMP: opcode + address (from SYMTAB or number)
   d. Write to output: LC, label, opcode, operand, object_code

3. Close files
```

**Key Functions:**

```c
// Look up mnemonic in OPTAB
struct OptabEntry* lookup_optab(char *mnemonic) {
    for (i = 0; i < OPTAB_SIZE; i++) {
        if (strcasecmp(mnemonic, OPTAB[i].mnemonic) == 0)
            return &OPTAB[i];
    }
    return NULL;  // Not found
}

// Get register code
int get_reg_code(char *r) {
    if (strcasecmp(r, "A") == 0) return 7;
    if (strcasecmp(r, "B") == 0) return 0;
    // ... etc
}

// Look up label in symbol table
int lookup_symbol(struct Symtab *tab, char *label) {
    for (i = 0; i < tab->count; i++) {
        if (strcmp(tab->entries[i].label, label) == 0)
            return tab->entries[i].address;
    }
    return -1;  // Not found
}
```

**Example Trace:**

Source: `sample_loop.asm`
```asm
START 1000H
LXI H, 2000H
MVI A, 0
LOOP INR A
     DCR M
     JNZ LOOP
     HLT
END
```

**Pass 1 builds SYMTAB:**
```
Label    Address
LOOP     1005H
```

**Pass 2 generates:**
```
Loc   Opcode  Operand    Object Code
1000  LXI     H,2000H    21 00 20
1003  MVI     A,0        3E 00
1005  INR     A          3C
1006  DCR     M          35
1007  JNZ     LOOP       C2 05 10
100A  HLT                76
```

### Viva Prep

**Q: Why do we need a two-pass assembler?**
A: To handle forward references. When a label is used before it's defined, Pass 1 builds symbol table first, then Pass 2 can resolve all addresses.

**Q: What is OPTAB?**
A: Operation Table. Static table containing all valid mnemonics with their opcodes and instruction lengths. Used to validate opcodes and get machine code.

**Q: What is SYMTAB?**
A: Symbol Table. Dynamic table built during Pass 1. Maps label names to their memory addresses.

**Q: What is Location Counter?**
A: LC keeps track of current memory address during assembly. Starts at START address, incremented by each instruction's length.

**Q: What is a forward reference?**
A: Using a label before it's defined. Example: `JMP END` appearing before the `END` label in code.

**Q: Explain MVI A, 05H encoding.**
A: MVI format: `00 DDD 110` where DDD = register code.
- A has code 111
- So opcode = 00 111 110 = 3EH
- Data = 05H
- Final: `3E 05`

**Q: What is little-endian?**
A: Lower byte stored at lower address. Address 2000H stored as `00 20` (not `20 00`). 8085 uses little-endian.

**Q: Difference between Pass 1 and Pass 2?**
A: Pass 1: Builds symbol table, calculates addresses, validates opcodes.
   Pass 2: Generates actual machine code using symbol table.

**Q: What are assembler directives?**
A: Instructions for the assembler, not the CPU.
- START/ORG: Set starting address
- END: End of program
- BYTE/WORD: Define data
- RESB/RESW: Reserve memory space

**Q: How is JNZ LOOP encoded?**
A: JNZ opcode = C2H. If LOOP = 1005H, then: `C2 05 10` (little-endian).

---

## Quick Reference

### How to Compile and Run

```bash
# Question 1
gcc 1_arithmetic_expression.c -o expr_analyzer
./expr_analyzer

# Question 2  
gcc 2_comment_identifier.c -o comment_check
./comment_check

# Question 3
cd assembler
gcc Assembler.c Pass_1.c Pass_2.c -o assembler
./assembler sample_loop.asm
```

### Files in Lab2/

| File | Purpose |
|------|---------|
| `1_arithmetic_expression.c` | Q1: Expression analyzer |
| `2_comment_identifier.c` | Q2: Comment detector |
| `assembler/Assembler.c` | Q3: Main + OPTAB |
| `assembler/Pass_1.c` | Q3: Build SYMTAB |
| `assembler/Pass_2.c` | Q3: Generate object code |
| `assembler/assembler.h` | Q3: Data structures |

### Important Header Files

| Header | Functions Used |
|--------|----------------|
| `<stdio.h>` | printf, scanf, fgets, fopen, fprintf |
| `<string.h>` | strcmp, strcpy, strlen, strstr, strcasecmp |
| `<ctype.h>` | isalpha, isalnum, isdigit, isspace |
| `<stdlib.h>` | atoi, strtol |
