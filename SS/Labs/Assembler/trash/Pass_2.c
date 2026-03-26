// Pass 2: Generate object code
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "assembler.h"

// Get register code: B=0, C=1, D=2, E=3, H=4, L=5, M=6, A=7
int get_reg_code(char *r) {
    if (strcasecmp(r, "B") == 0) return 0;
    if (strcasecmp(r, "C") == 0) return 1;
    if (strcasecmp(r, "D") == 0) return 2;
    if (strcasecmp(r, "E") == 0) return 3;
    if (strcasecmp(r, "H") == 0) return 4;
    if (strcasecmp(r, "L") == 0) return 5;
    if (strcasecmp(r, "M") == 0) return 6;
    if (strcasecmp(r, "A") == 0) return 7;
    return -1;
}

// Get register pair code: B=0, D=1, H=2, SP=3
int get_rp_code(char *rp) {
    if (strcasecmp(rp, "B") == 0) return 0;
    if (strcasecmp(rp, "D") == 0) return 1;
    if (strcasecmp(rp, "H") == 0) return 2;
    if (strcasecmp(rp, "SP") == 0) return 3;
    return -1;
}

// Parse number with H suffix
int parse_num(char *s) {
    int len = strlen(s);
    while (s[0] == ' ') s++;
    if (len > 0 && (s[len-1] == 'H' || s[len-1] == 'h')) {
        s[len-1] = '\0';
        return (int)strtol(s, NULL, 16);
    }
    return atoi(s);
}

// Lookup symbol in table
int lookup_symbol(struct Symtab *tab, char *label) {
    int i;
    for (i = 0; i < tab->count; i++) {
        if (strcmp(tab->entries[i].label, label) == 0)
            return tab->entries[i].address;
    }
    return -1;
}

// Get address from operand (symbol or number)
int get_address(char *operand, struct Symtab *symtab) {
    int addr = lookup_symbol(symtab, operand);
    if (addr >= 0) return addr;
    return parse_num(operand);
}

// Split "A, 05H" into reg and value
void split_operand(char *operand, char *left, char *right) {
    char *comma = strchr(operand, ',');
    if (comma) {
        strncpy(left, operand, comma - operand);
        left[comma - operand] = '\0';
        strcpy(right, comma + 1);
        // Trim spaces
        while (left[0] == ' ') memmove(left, left+1, strlen(left));
        while (right[0] == ' ') memmove(right, right+1, strlen(right));
    } else {
        strcpy(left, operand);
        right[0] = '\0';
    }
}

int pass2(char *intermediate, char *output, struct Pass1Result *p1) {
    FILE *in, *out;
    char line[100];
    int loc;
    char label[20], opcode[20], operand[50];
    char objcode[30];
    char left[20], right[20];
    int op_byte, addr;
    struct OptabEntry *entry;
    
    in = fopen(intermediate, "r");
    out = fopen(output, "w");
    if (!in || !out) {
        printf("Error opening files\n");
        return -1;
    }
    
    fprintf(out, "Loc\tLabel\t\tOpcode\t\tOperand\t\tObject Code\n");
    fprintf(out, "----\t-----\t\t------\t\t-------\t\t-----------\n");
    
    while (fgets(line, sizeof(line), in)) {
        objcode[0] = '\0';
        
        sscanf(line, "%x %s %s %[^\n]", &loc, label, opcode, operand);
        
        // Skip START and END
        if (strcasecmp(opcode, "START") == 0) {
            fprintf(out, "%04X\t%-10s\t%-10s\t%-10s\t-\n", loc, 
                strcmp(label, "-") ? label : "", opcode, operand);
            continue;
        }
        if (strcasecmp(opcode, "END") == 0) {
            fprintf(out, "%04X\t%-10s\t%-10s\t%-10s\t-\n", loc,
                strcmp(label, "-") ? label : "", opcode, "");
            break;
        }
        
        entry = lookup_optab(opcode);
        
        if (entry != NULL) {
            switch (entry->kind) {
            
            case IK_FIXED:  // NOP, HLT
                sprintf(objcode, "%02X", entry->opcode);
                break;
                
            case IK_MVI:  // MVI r, data
                split_operand(operand, left, right);
                op_byte = 0x06 | (get_reg_code(left) << 3);
                sprintf(objcode, "%02X %02X", op_byte, parse_num(right) & 0xFF);
                break;
                
            case IK_LXI:  // LXI rp, data16
                split_operand(operand, left, right);
                op_byte = 0x01 | (get_rp_code(left) << 4);
                addr = get_address(right, &p1->symtab);
                sprintf(objcode, "%02X %02X %02X", op_byte, addr & 0xFF, (addr >> 8) & 0xFF);
                break;
                
            case IK_DIRECT:  // LDA, STA
                addr = get_address(operand, &p1->symtab);
                sprintf(objcode, "%02X %02X %02X", entry->opcode, addr & 0xFF, (addr >> 8) & 0xFF);
                break;
                
            case IK_JUMP:  // JMP, JZ, JNZ
                addr = get_address(operand, &p1->symtab);
                sprintf(objcode, "%02X %02X %02X", entry->opcode, addr & 0xFF, (addr >> 8) & 0xFF);
                break;
                
            case IK_MOV:  // MOV r1, r2
                split_operand(operand, left, right);
                op_byte = 0x40 | (get_reg_code(left) << 3) | get_reg_code(right);
                sprintf(objcode, "%02X", op_byte);
                break;
                
            case IK_REG:  // ADD, SUB
                op_byte = entry->opcode | get_reg_code(operand);
                sprintf(objcode, "%02X", op_byte);
                break;
                
            case IK_INRDCR:  // INR, DCR
                op_byte = entry->opcode | (get_reg_code(operand) << 3);
                sprintf(objcode, "%02X", op_byte);
                break;
            }
        }
        else if (strcasecmp(opcode, "WORD") == 0) {
            addr = get_address(operand, &p1->symtab);
            sprintf(objcode, "%02X %02X", addr & 0xFF, (addr >> 8) & 0xFF);
        }
        else if (strcasecmp(opcode, "BYTE") == 0) {
            sprintf(objcode, "%02X", parse_num(operand) & 0xFF);
        }
        else if (strcasecmp(opcode, "RESB") == 0 || strcasecmp(opcode, "RESW") == 0) {
            strcpy(objcode, "--");
        }
        
        // Write output line
        fprintf(out, "%04X\t%-10s\t%-10s\t%-10s\t%s\n", loc,
            strcmp(label, "-") ? label : "", opcode,
            strcmp(operand, "-") ? operand : "", objcode);
    }
    
    fclose(in);
    fclose(out);
    return 0;
}
