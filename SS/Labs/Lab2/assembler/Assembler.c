// Two-Pass 8085 Assembler - Main Program
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "assembler.h"

// OPTAB - 8085 instruction set
struct OptabEntry OPTAB[] = {
    {"NOP",  0x00, 1, IK_FIXED},
    {"HLT",  0x76, 1, IK_FIXED},
    {"MVI",  0x00, 2, IK_MVI},
    {"LXI",  0x01, 3, IK_LXI},
    {"LDA",  0x3A, 3, IK_DIRECT},
    {"STA",  0x32, 3, IK_DIRECT},
    {"JMP",  0xC3, 3, IK_JUMP},
    {"JZ",   0xCA, 3, IK_JUMP},
    {"JNZ",  0xC2, 3, IK_JUMP},
    {"JC",   0xDA, 3, IK_JUMP},
    {"JNC",  0xD2, 3, IK_JUMP},
    {"MOV",  0x40, 1, IK_MOV},
    {"ADD",  0x80, 1, IK_REG},
    {"SUB",  0x90, 1, IK_REG},
    {"INR",  0x04, 1, IK_INRDCR},
    {"DCR",  0x05, 1, IK_INRDCR},
};

int OPTAB_SIZE = 16;

// Search OPTAB for mnemonic
struct OptabEntry* lookup_optab(char *mnemonic) {
    int i;
    for (i = 0; i < OPTAB_SIZE; i++) {
        if (strcasecmp(mnemonic, OPTAB[i].mnemonic) == 0)
            return &OPTAB[i];
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    struct Pass1Result p1 = {0};
    
    if (argc != 2) {
        printf("Usage: %s <source.asm>\n", argv[0]);
        return 1;
    }
    
    printf("\n=== Two-Pass 8085 Assembler ===\n\n");
    
    // Pass 1
    printf("Running Pass 1...\n");
    if (pass1(argv[1], "intermediate.int", &p1) != 0) {
        printf("Pass 1 failed\n");
        return 1;
    }
    printf("Pass 1 complete.\n");
    print_symtab(&p1.symtab);
    
    // Pass 2
    printf("\nRunning Pass 2...\n");
    if (pass2("intermediate.int", "output.obj", &p1) != 0) {
        printf("Pass 2 failed\n");
        return 1;
    }
    
    printf("\nAssembly complete!\n");
    printf("Output: intermediate.int, output.obj\n");
    
    return 0;
}
