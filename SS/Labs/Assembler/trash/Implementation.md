# 2-Pass 8085 Assembler in C — Work Plan

## Overview

A **2-Pass Assembler** reads source assembly code twice:

- **Pass 1**: Build a Symbol Table (resolves forward references). Assign addresses to labels.
- **Pass 2**: Generate machine code using the symbol table from Pass 1.

The user provides the **starting address**. Output will be a listing file showing addresses, machine code (hex), and the original source.

---

## Files to be Created

All files go into a single folder (e.g., `8085_assembler/`).

| File | Purpose |
|---|---|
| `main.c` | Entry point — reads input file, calls Pass 1 then Pass 2 |
| `pass1.c` | Pass 1 logic — builds symbol table, assigns addresses |
| `pass2.c` | Pass 2 logic — generates machine code |
| `opcode_table.c` | Hardcoded 8085 instruction set (mnemonic → opcode, size) |
| `opcode_table.h` | Header for opcode table |
| `symbol_table.c` | Symbol table (labels → addresses) using simple array |
| `symbol_table.h` | Header for symbol table |
| `utils.c` | Helpers: string trimming, uppercase conversion, comment stripping |
| `utils.h` | Header for utils |
| `assembler.h` | Shared structs and constants |
| `Makefile` | To compile easily with `make` |

---

## Key Data Structures

### Opcode Table Entry
```c
typedef struct {
    char mnemonic[20]; // e.g., "MOV", "MVI"
    char opcode[3];    // e.g., 0x3E
    int  size;         // bytes: 1, 2, or 3
} OpcodeEntry;
```

### Symbol Table Entry
```c
typedef struct {
    char label[20];
    int  address;
} Symbol;
```

### Source Line (Intermediate)
```c
typedef struct {
    int  address;
    char label[20];
    char mnemonic[20];
    char operand[30];
} Line;
```

---

## What Each Pass Does

### Pass 1 — Symbol Table Builder
1. Read each line of source code
2. Strip comments (`;`), blank lines
3. Check for **label** (ends with `:`) → add to symbol table with current address
4. Look up mnemonic in opcode table → get instruction size
5. Increment Location Counter (LC) by instruction size
6. Handle `ORG` directive to change LC
7. Handle `END` to stop

### Pass 2 — Code Generator
1. Re-read each line (or use intermediate output from Pass 1)
2. Look up mnemonic → get opcode
3. Resolve operand: if it's a label, look it up in the symbol table
4. Handle register-based opcodes (`MOV r1,r2`, `MVI r,data`, etc.)
5. Write output: `ADDRESS  OPCODE  SOURCE_LINE`

---

## Supported 8085 Instructions (Complete Set)

Categories to implement:
- **Data Transfer**: MOV, MVI, LDA, STA, LHLD, SHLD, XCHG, etc.
- **Arithmetic**: ADD, ADI, SUB, SUI, INR, DCR, DAD, INX, DCX, etc.
- **Logical**: ANA, ANI, ORA, ORI, XRA, XRI, CMP, CPI, etc.
- **Branch**: JMP, JZ, JNZ, JC, JNC, JM, JP, JP, CALL, RET, etc.
- **Stack**: PUSH, POP, XTHL, SPHL, etc.
- **I/O & Machine**: IN, OUT, HLT, NOP, EI, DI, SIM, RIM, etc.

---

## Assembler Directives (Pseudo Instructions)
- `ORG <addr>` — Set starting address
- `DB <data>` — Define byte
- `DW <data>` — Define word
- `END` — End of program

---

## Sample Input (`input.asm`)
```asm
        ORG 2000H
START:  MVI A, 05H
        MOV B, A
        LXI H, 3000H
LOOP:   ADD B
        JNZ LOOP
        HLT
        END
```

## Sample Output (`output.lst`)
```
ADDRESS  CODE        SOURCE
2000     3E 05       MVI A, 05H
2002     47          MOV B, A
2003     21 00 30    LXI H, 3000H
2006     80          ADD B
2007     C2 06 20    JNZ LOOP
200A     76          HLT
```

---

## Compilation
```bash
make
./assembler input.asm
```

---

## Scope (B.Tech Level)
- No macro support
- No complex expression evaluation
- Labels are simple identifiers (letters/digits)
- All values in hex (with `H` suffix) or decimal
- Max 100 labels in symbol table
- Max 200 lines in source
