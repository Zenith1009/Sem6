/*
 * symbol_table.c
 * Simple array-based symbol table for the 2-Pass 8085 Assembler
 */

#include "assembler.h"

/* Initialize the symbol table */
void symtab_init(SymbolTable *st) {
    st->count = 0;
}

/*
 * symtab_add: Add a (label, address) pair to the table.
 * Returns 0 on success, -1 if table is full or label already exists.
 */
int symtab_add(SymbolTable *st, const char *label, int address) {
    int i;
    /* Check for duplicate */
    for (i = 0; i < st->count; i++) {
        if (strcasecmp(st->entries[i].label, label) == 0) {
            fprintf(stderr, "Error: Duplicate label '%s'\n", label);
            return -1;
        }
    }
    if (st->count >= MAX_LABELS) {
        fprintf(stderr, "Error: Symbol table full (max %d labels)\n", MAX_LABELS);
        return -1;
    }
    strncpy(st->entries[st->count].label, label, MAX_LABEL_LEN - 1);
    st->entries[st->count].label[MAX_LABEL_LEN - 1] = '\0';
    st->entries[st->count].address = address;
    st->count++;
    return 0;
}

/*
 * symtab_lookup: Search for a label.
 * Returns the address if found, or -1 if not found.
 */
int symtab_lookup(SymbolTable *st, const char *label) {
    int i;
    for (i = 0; i < st->count; i++) {
        if (strcasecmp(st->entries[i].label, label) == 0)
            return st->entries[i].address;
    }
    return -1;
}

/* Print the symbol table (for debugging) */
void symtab_print(SymbolTable *st) {
    int i;
    printf("\n+----------------------------+\n");
    printf("| SYMBOL TABLE               |\n");
    printf("+----------------------------+\n");
    printf("| %-18s | ADDR |\n", "LABEL");
    printf("+----------------------------+\n");
    for (i = 0; i < st->count; i++) {
        printf("| %-18s | %04X |\n",
               st->entries[i].label,
               st->entries[i].address);
    }
    printf("+----------------------------+\n");
}
