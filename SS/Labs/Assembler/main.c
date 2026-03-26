/*
 * main.c
 * Entry point for the 2-Pass 8085 Assembler
 *
 * Usage: ./assembler <source.asm>
 *
 * The user can specify the starting address via the 'ORG' directive
 * in their source file. If no ORG is given, assembly starts at 0000H.
 */

#include "assembler.h"

/* Forward declarations */
int pass1(const char *src_file, Pass1Result *result);
int pass2(Pass1Result *result, const char *out_file);
void symtab_print(SymbolTable *st);

int main(int argc, char *argv[]) {
    Pass1Result  p1_result;
    char         out_file[256];
    int          ret;

    /* ── Banner ─────────────────────────────────────────── */
    printf("==========================================\n");
    printf("       2-Pass 8085 Assembler              \n");
    printf("==========================================\n\n");

    if (argc != 2) {
        printf("Usage: %s <source.asm>\n", argv[0]);
        printf("Example: %s program.asm\n", argv[0]);
        return 1;
    }

    /* Build output filename: replace extension with .lst */
    {
        char *dot;
        strncpy(out_file, argv[1], sizeof(out_file) - 1);
        out_file[sizeof(out_file) - 1] = '\0';
        dot = strrchr(out_file, '.');
        if (dot) *dot = '\0';
        strncat(out_file, ".lst", sizeof(out_file) - strlen(out_file) - 1);
    }

    /* ── PASS 1 ──────────────────────────────────────────── */
    printf(">>> PASS 1: Building Symbol Table\n");
    printf("------------------------------------------\n");

    memset(&p1_result, 0, sizeof(p1_result));
    ret = pass1(argv[1], &p1_result);
    if (ret != 0) {
        printf("\n[PASS 1 FAILED] Fix errors above and retry.\n");
        return 1;
    }
    printf("------------------------------------------\n");
    printf("Pass 1 complete. %d line(s) processed.\n", p1_result.line_count);

    /* Print the symbol table */
    symtab_print(&p1_result.symtab);

    /* ── PASS 2 ──────────────────────────────────────────── */
    printf("\n>>> PASS 2: Generating Machine Code\n");
    printf("------------------------------------------\n");

    ret = pass2(&p1_result, out_file);
    if (ret != 0) {
        printf("\n[PASS 2 FAILED] Fix errors above and retry.\n");
        return 1;
    }

    printf("------------------------------------------\n");
    printf("\nAssembly successful!\n");
    printf("Output listing written to: %s\n\n", out_file);

    return 0;
}
