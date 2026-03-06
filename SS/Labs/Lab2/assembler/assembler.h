// Two-Pass 8085 Assembler - Header File
#ifndef ASSEMBLER_H
#define ASSEMBLER_H

#define MAX_SYMBOLS 50

// Instruction types
#define IK_FIXED    0   // NOP, HLT
#define IK_MVI      1   // MVI r, data
#define IK_LXI      2   // LXI rp, data16
#define IK_DIRECT   3   // LDA, STA addr
#define IK_JUMP     4   // JMP, JZ, JNZ addr
#define IK_MOV      5   // MOV r1, r2
#define IK_REG      6   // ADD, SUB r
#define IK_INRDCR   7   // INR, DCR r

// OPTAB entry
struct OptabEntry {
    char mnemonic[10];
    int opcode;
    int length;
    int kind;
};

// Symbol table entry
struct SymEntry {
    char label[20];
    int address;
};

// Symbol table
struct Symtab {
    struct SymEntry entries[MAX_SYMBOLS];
    int count;
};

// Pass 1 result
struct Pass1Result {
    struct Symtab symtab;
    int start_addr;
};

// Function declarations
struct OptabEntry* lookup_optab(char *mnemonic);
int pass1(char *source, char *intermediate, struct Pass1Result *result);
int pass2(char *intermediate, char *output, struct Pass1Result *p1);
void print_symtab(struct Symtab *symtab);

#endif
