/*
 * assembler.h
 * Shared definitions, structs, and function prototypes for the 2-Pass 8085 Assembler
 */

#ifndef ASSEMBLER_H
#define ASSEMBLER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Limits
#define MAX_LABELS      200
#define MAX_LINES       500
#define MAX_LINE_LEN    100
#define MAX_MNEMONIC    15
#define MAX_OPERAND     30
#define MAX_LABEL_LEN   20

// Instruction Kinds
typedef enum {
    IK_FIXED,    /* No operands: NOP, HLT, RET, XCHG, etc.          */
    IK_MOV,      /* MOV r1, r2  — both registers                     */
    IK_MVI,      /* MVI r, data — register + 8-bit immediate         */
    IK_LXI,      /* LXI rp, data16 — register pair + 16-bit imm     */
    IK_REG,      /* ADD/SUB/ANA etc. with single register operand    */
    IK_INRDCR,   /* INR/DCR r — single register                      */
    IK_DIRECT,   /* LDA/STA/LHLD/SHLD — 16-bit direct address       */
    IK_JUMP,     /* JMP/CALL/Jcond — 16-bit address (label or addr)  */
    IK_PUSH_POP, /* PUSH/POP rp                                       */
    IK_IO,       /* IN/OUT — 8-bit port number                       */
    IK_RST,      /* RST n                                             */
    IK_DB,       /* Pseudo: define byte                               */
    IK_DW,       /* Pseudo: define word                               */
    IK_ORG,      /* Pseudo: set location counter                      */
    IK_END       /* Pseudo: end of program                            */
} InstrKind;

// Opcode Table Entry
typedef struct {
    char       mnemonic[MAX_MNEMONIC];
    unsigned char opcode;   /* Base opcode (registers encoded at runtime) */
    int        size;        /* Bytes: 1, 2, or 3 */
    InstrKind  kind;
} OpcodeEntry;

// Symbol Table Entry
typedef struct {
    char label[MAX_LABEL_LEN];
    int  address;
} Symbol;

// Symbol Table
typedef struct {
    Symbol entries[MAX_LABELS];
    int    count;
} SymbolTable;

// Intermediate Line (Pass 1 → Pass 2)
typedef struct {
    int  address;
    char label[MAX_LABEL_LEN];
    char mnemonic[MAX_MNEMONIC];
    char operand[MAX_OPERAND];
    int  line_no;
} Line;

// Pass 1 Result
typedef struct {
    SymbolTable symtab;
    Line        lines[MAX_LINES];
    int         line_count;
} Pass1Result;

// Function Prototypes

// opcode_table.c
OpcodeEntry* lookup_opcode(const char *mnemonic);
int          get_reg_code(const char *reg);
int          get_rp_code(const char *rp);

/* symbol_table.c */
void  symtab_init(SymbolTable *st);
int   symtab_add(SymbolTable *st, const char *label, int address);
int   symtab_lookup(SymbolTable *st, const char *label);
void  symtab_print(SymbolTable *st);

/* utils.c */
void str_trim(char *s);
void str_upper(char *s);
void strip_comment(char *s);
int  parse_number(const char *s);
int  is_valid_label(const char *s);
void split_operands(const char *operand, char *op1, char *op2);

/* pass1.c */
int pass1(const char *src_file, Pass1Result *result);

/* pass2.c */
int pass2(Pass1Result *result, const char *out_file);

#endif /* ASSEMBLER_H */
