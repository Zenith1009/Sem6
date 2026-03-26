/*
 * symbol_table.h
 */
#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H

#include "assembler.h"

void  symtab_init(SymbolTable *st);
int   symtab_add(SymbolTable *st, const char *label, int address);
int   symtab_lookup(SymbolTable *st, const char *label);
void  symtab_print(SymbolTable *st);

#endif
