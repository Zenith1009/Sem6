// Pass 1: Build symbol table, write intermediate file
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "assembler.h"

// Remove leading/trailing spaces
void trim(char *s) {
    int i = 0, j = 0;
    while (s[i] == ' ' || s[i] == '\t') i++;
    while (s[i]) s[j++] = s[i++];
    s[j] = '\0';
    while (j > 0 && (s[j-1] == ' ' || s[j-1] == '\n' || s[j-1] == '\r'))
        s[--j] = '\0';
}

// Parse number (decimal or hex with H suffix)
int parse_number(char *s) {
    int len = strlen(s);
    if (len > 0 && (s[len-1] == 'H' || s[len-1] == 'h')) {
        s[len-1] = '\0';
        return (int)strtol(s, NULL, 16);
    }
    return atoi(s);
}

// Check if string is a directive
int is_directive(char *op) {
    if (strcasecmp(op, "START") == 0) return 1;
    if (strcasecmp(op, "END") == 0) return 1;
    if (strcasecmp(op, "BYTE") == 0) return 1;
    if (strcasecmp(op, "WORD") == 0) return 1;
    if (strcasecmp(op, "RESB") == 0) return 1;
    if (strcasecmp(op, "RESW") == 0) return 1;
    return 0;
}

// Add symbol to table
int add_symbol(struct Symtab *tab, char *label, int addr) {
    int i;
    // Check for duplicate
    for (i = 0; i < tab->count; i++) {
        if (strcmp(tab->entries[i].label, label) == 0) {
            printf("Error: Duplicate label %s\n", label);
            return -1;
        }
    }
    strcpy(tab->entries[tab->count].label, label);
    tab->entries[tab->count].address = addr;
    tab->count++;
    return 0;
}

int pass1(char *source, char *intermediate, struct Pass1Result *result) {
    FILE *src, *out;
    char line[100], label[20], opcode[20], operand[50];
    char first[20], rest[80];
    int loc = 0;
    
    src = fopen(source, "r");
    out = fopen(intermediate, "w");
    if (!src || !out) {
        printf("Error opening files\n");
        return -1;
    }
    
    result->symtab.count = 0;
    
    while (fgets(line, sizeof(line), src)) {
        // Remove newline, skip blank lines
        line[strlen(line)-1] = '\0';
        trim(line);
        if (line[0] == '\0' || line[0] == '.') continue;
        
        // Initialize
        label[0] = opcode[0] = operand[0] = '\0';
        first[0] = rest[0] = '\0';
        
        // Parse line
        sscanf(line, "%s %[^\n]", first, rest);
        trim(rest);
        
        // Check if first word is opcode or label
        if (lookup_optab(first) != NULL || is_directive(first)) {
            strcpy(opcode, first);
            strcpy(operand, rest);
        } else {
            strcpy(label, first);
            sscanf(rest, "%s %[^\n]", opcode, operand);
            trim(operand);
        }
        
        // Handle START
        if (strcasecmp(opcode, "START") == 0) {
            loc = parse_number(operand);
            result->start_addr = loc;
            fprintf(out, "%04X\t%s\t%s\t%s\n", loc, 
                label[0] ? label : "-", opcode, operand);
            continue;
        }
        
        // Add label to symbol table
        if (label[0] != '\0') {
            if (add_symbol(&result->symtab, label, loc) != 0)
                return -1;
        }
        
        // Get instruction length
        int len = 0;
        struct OptabEntry *entry = lookup_optab(opcode);
        
        if (entry != NULL) {
            len = entry->length;
        }
        else if (strcasecmp(opcode, "WORD") == 0) {
            len = 2;
        }
        else if (strcasecmp(opcode, "BYTE") == 0) {
            len = 1;
        }
        else if (strcasecmp(opcode, "RESB") == 0) {
            len = parse_number(operand);
        }
        else if (strcasecmp(opcode, "RESW") == 0) {
            len = 2 * parse_number(operand);
        }
        else if (strcasecmp(opcode, "END") == 0) {
            fprintf(out, "%04X\t%s\t%s\t%s\n", loc,
                label[0] ? label : "-", opcode, "-");
            break;
        }
        else {
            printf("Error: Unknown opcode %s\n", opcode);
            return -1;
        }
        
        // Write to intermediate file
        fprintf(out, "%04X\t%s\t%s\t%s\n", loc,
            label[0] ? label : "-", opcode, operand[0] ? operand : "-");
        loc += len;
    }
    
    fclose(src);
    fclose(out);
    return 0;
}

void print_symtab(struct Symtab *symtab) {
    int i;
    printf("\nSYMTAB:\n");
    printf("Label\t\tAddress\n");
    printf("-----\t\t-------\n");
    for (i = 0; i < symtab->count; i++) {
        printf("%-10s\t%04X\n", 
            symtab->entries[i].label, 
            symtab->entries[i].address);
    }
}
