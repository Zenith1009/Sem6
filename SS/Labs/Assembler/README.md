# System Software Labs: 2-Pass 8085 Assembler

## Table of Contents
- [1. Overview](#1-overview)
- [2. How a 2-Pass Assembler Works](#2-how-a-2-pass-assembler-works)
- [3. File Structure](#3-file-structure)
- [4. Key Data Structures](#4-key-data-structures)
- [5. Supported Instructions](#5-supported-instructions)
- [6. Assembler Directives](#6-assembler-directives)
- [7. Forward Reference Resolution](#7-forward-reference-resolution)
- [8. Sample Input and Output](#8-sample-input-and-output)
- [9. Compile and Run](#9-compile-and-run)

---

## 1. Overview

A 2-Pass Assembler for the **Intel 8085 microprocessor** written in C.

- Accepts `.asm` source files and produces a `.lst` listing file.
- Supports the **complete 8085 instruction set** (~90 instructions).
- Resolves **forward references** (using a label before it is defined).
- Starting address is set via the `ORG` directive in the source file.

---

## 2. How a 2-Pass Assembler Works

```
Source File (.asm)
       │
       ▼
  ┌─────────┐    builds     ┌──────────────┐
  │  Pass 1 │ ─────────────►│ Symbol Table │
  └─────────┘               │ (label→addr) │
       │                    └──────────────┘
       │                          │
       ▼                          ▼
  ┌─────────┐    uses       ┌─────────────┐
  │  Pass 2 │ ─────────────►│ Output .lst │
  └─────────┘               └─────────────┘
```

**Pass 1 — Symbol Table Builder**
1. Read each line; strip comments and blank lines.
2. If a label is found (ends with `:`), add it to the symbol table with the current **Location Counter (LC)**.
3. Look up the mnemonic in the opcode table to get instruction size.
4. Advance LC by instruction size.
5. Handle `ORG` (set LC), `END` (stop), `DB`/`DW` (data bytes).

**Pass 2 — Code Generator**
1. Re-process every stored line using the complete symbol table.
2. Encode operands: registers are OR-ed into the base opcode; labels are resolved from the symbol table.
3. Write the listing: `ADDRESS | HEX BYTES | SOURCE LINE`.

Forward references are resolved because the **symbol table is fully built in Pass 1 before any code is generated in Pass 2**.

---

## 3. File Structure

```
Assembler/
├── assembler.h        # Shared structs, enums, constants, prototypes
├── opcode_table.h/c   # Complete 8085 opcode table (~90 instructions)
├── symbol_table.h/c   # Label -> address table (add, lookup, print)
├── utils.h/c          # String helpers: trim, uppercase, parse numbers
├── pass1.c            # Pass 1: symbol table builder + LC tracker
├── pass2.c            # Pass 2: machine code generator
├── main.c             # Entry point
├── Makefile           # Build system
└── test.asm           # Sample program with forward references
```

---

## 4. Key Data Structures

```c
/* Opcode table entry */
typedef struct {
    char      mnemonic[15];
    unsigned char opcode;    /* Base opcode */
    int       size;          /* Bytes: 1, 2, or 3 */
    InstrKind kind;          /* Encoding category */
} OpcodeEntry;

/* Symbol table entry */
typedef struct {
    char label[20];
    int  address;
} Symbol;

/* Parsed source line (stored by Pass 1, consumed by Pass 2) */
typedef struct {
    int  address;
    char label[20];
    char mnemonic[15];
    char operand[30];
    int  line_no;
} Line;
```

Register encoding follows the 8085 standard:
`B=0, C=1, D=2, E=3, H=4, L=5, M=6, A=7`

---

## 5. Supported Instructions

| Category | Instructions |
|---|---|
| Data Transfer | `MOV`, `MVI`, `LXI`, `LDA`, `STA`, `LHLD`, `SHLD`, `LDAX`, `STAX`, `XCHG` |
| Arithmetic | `ADD`, `ADI`, `ADC`, `ACI`, `SUB`, `SUI`, `SBB`, `SBI`, `INR`, `DCR`, `INX`, `DCX`, `DAD`, `DAA` |
| Logical | `ANA`, `ANI`, `ORA`, `ORI`, `XRA`, `XRI`, `CMP`, `CPI`, `RLC`, `RRC`, `RAL`, `RAR`, `CMA`, `CMC`, `STC` |
| Branch | `JMP`, `JZ`, `JNZ`, `JC`, `JNC`, `JPE`, `JPO`, `JM`, `JP`, `CALL`, `CZ`, `CNZ`, `CC`, `CNC`, `RET`, `RZ`, `RNZ`, `RC`, `RNC`, `PCHL`, `RST` |
| Stack | `PUSH`, `POP`, `XTHL`, `SPHL` |
| I/O & Control | `IN`, `OUT`, `HLT`, `NOP`, `EI`, `DI`, `RIM`, `SIM` |

---

## 6. Assembler Directives

| Directive | Description |
|---|---|
| `ORG addr` | Set Location Counter to `addr` (starting address) |
| `DB data` | Define a single byte in memory |
| `DW data` | Define a 16-bit word in memory (little-endian) |
| `END` | Mark end of source program |

---

## 7. Forward Reference Resolution

A **forward reference** occurs when a label is used (e.g., in a jump) before it is defined.  
This assembler resolves them because:

- **Pass 1** scans the *entire* source and records every label's address into the symbol table.
- **Pass 2** only runs *after* Pass 1 is complete, so all labels are already known.

Example:
```asm
        JZ  DONE       ; DONE not defined yet — forward reference
        NOP
DONE:   HLT            ; DONE defined here
```
Pass 1 records `DONE = 2005H`. Pass 2 fills in `CA 05 20` for the `JZ` instruction.

---

## 8. Sample Input and Output

### Input (`test.asm`)
```asm
        ORG 2000H
START:  MVI A, 05H
        LXI H, 3000H
        JZ  DONE           ; forward reference
LOOP:   DCR C
        JNZ LOOP
DONE:   HLT
        END
```

### Output (Pass 1 — Symbol Table)
```
| LABEL  | ADDR |
| START  | 2000 |
| LOOP   | 2007 |
| DONE   | 200A |
```

### Output (Pass 2 — Listing)
```
ADDR  HEX CODE      SOURCE
2000  3E 05         START: MVI A, 05H
2002  21 00 30      LXI H, 3000H
2005  CA 0A 20      JZ DONE           <-- forward ref resolved
2008  0D            LOOP: DCR C
2009  C2 08 20      JNZ LOOP
200A  76            DONE: HLT
```

---

## 9. Compile and Run

```bash
cd SS/Labs/Assembler

# Build
make

# Assemble a file
./assembler test.asm 2>&1

# Output is written to test.lst
cat test.lst

# Clean build artifacts
make clean
```

Number formats accepted in operands:
- Hex with `H` suffix: `2000H`, `0FFH`
- Hex with `0x` prefix: `0x2000`
- Decimal: `100`
