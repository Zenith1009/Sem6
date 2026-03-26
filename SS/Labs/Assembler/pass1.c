/*
 * pass1.c
 *
 * PASS 1 — Symbol Table Builder
 *
 * Steps:
 *   1. Read each source line
 *   2. Strip comments, skip blank lines
 *   3. If a label is found, add it to the symbol table with current LC
 *   4. Look up mnemonic → get instruction size → advance LC
 *   5. Handle ORG (change LC), END (stop), DB/DW (define data)
 *   6. Store parsed lines in Pass1Result for Pass 2 to use
 */

#include "assembler.h"
#include "utils.h"

/* ── Helpers ──────────────────────────────────────────── */

/* Parse a source line into label, mnemonic, operand */
static void parse_line(char *raw, char *label, char *mnemonic, char *operand) {
    char buf[MAX_LINE_LEN];
    char *tok;

    label[0] = mnemonic[0] = operand[0] = '\0';

    strncpy(buf, raw, MAX_LINE_LEN - 1);
    buf[MAX_LINE_LEN - 1] = '\0';

    str_trim(buf);

    /* Check for label: first token ending with ':' */
    tok = strtok(buf, " \t");
    if (!tok) return;

    int len = (int)strlen(tok);
    if (tok[len - 1] == ':') {
        /* It's a label */
        tok[len - 1] = '\0';
        str_upper(tok);
        strncpy(label, tok, MAX_LABEL_LEN - 1);
        label[MAX_LABEL_LEN - 1] = '\0';

        /* Next token is the mnemonic */
        tok = strtok(NULL, " \t");
        if (!tok) return;
    }

    /* Mnemonic */
    str_upper(tok);
    strncpy(mnemonic, tok, MAX_MNEMONIC - 1);
    mnemonic[MAX_MNEMONIC - 1] = '\0';

    /* Everything after mnemonic is the operand */
    tok = strtok(NULL, "\n");
    if (tok) {
        str_trim(tok);
        str_upper(tok);
        strncpy(operand, tok, MAX_OPERAND - 1);
        operand[MAX_OPERAND - 1] = '\0';
    }
}

/* ── Main Pass 1 Function ─────────────────────────────── */
int pass1(const char *src_file, Pass1Result *result) {
    FILE *fp;
    char  raw[MAX_LINE_LEN];
    char  label[MAX_LABEL_LEN];
    char  mnemonic[MAX_MNEMONIC];
    char  operand[MAX_OPERAND];
    int   lc;         /* Location Counter */
    int   line_no = 0;
    int   error   = 0;

    fp = fopen(src_file, "r");
    if (!fp) {
        fprintf(stderr, "Error: Cannot open source file '%s'\n", src_file);
        return -1;
    }

    /* Initialize */
    symtab_init(&result->symtab);
    result->line_count = 0;
    lc = 0;  /* Will be set by ORG or user-provided start */

    printf("%-6s %-20s %-12s %-20s %-8s\n",
           "LINE", "LABEL", "MNEMONIC", "OPERAND", "ADDR");
    printf("---------------------------------------------------------------\n");

    while (fgets(raw, MAX_LINE_LEN, fp)) {
        line_no++;

        /* Strip comment and trailing whitespace */
        strip_comment(raw);

        /* Skip blank lines */
        if (strlen(raw) == 0) continue;

        /* Parse into components */
        parse_line(raw, label, mnemonic, operand);

        /* Skip if nothing was parsed (comment-only line) */
        if (mnemonic[0] == '\0' && label[0] == '\0') continue;

        /* ── Handle Label ──────────────────────────────── */
        if (label[0] != '\0') {
            if (symtab_add(&result->symtab, label, lc) != 0) {
                fprintf(stderr, "  at line %d\n", line_no);
                error = 1;
            }
        }

        /* Skip if only a label and no mnemonic (label-only line) */
        if (mnemonic[0] == '\0') continue;

        /* Print Pass 1 trace */
        printf("%-6d %-20s %-12s %-20s %04X\n",
               line_no, label, mnemonic, operand, lc);

        /* ── Store this line ───────────────────────────── */
        if (result->line_count >= MAX_LINES) {
            fprintf(stderr, "Error: Too many lines (max %d)\n", MAX_LINES);
            fclose(fp);
            return -1;
        }
        result->lines[result->line_count].address = lc;
        result->lines[result->line_count].line_no  = line_no;
        strncpy(result->lines[result->line_count].label,    label,    MAX_LABEL_LEN - 1);
        strncpy(result->lines[result->line_count].mnemonic, mnemonic, MAX_MNEMONIC - 1);
        strncpy(result->lines[result->line_count].operand,  operand,  MAX_OPERAND - 1);
        result->lines[result->line_count].label[MAX_LABEL_LEN - 1]    = '\0';
        result->lines[result->line_count].mnemonic[MAX_MNEMONIC - 1]  = '\0';
        result->lines[result->line_count].operand[MAX_OPERAND - 1]    = '\0';
        result->line_count++;

        /* ── Update Location Counter ───────────────────── */
        if (strcmp(mnemonic, "ORG") == 0) {
            /* Set LC to the given address */
            lc = parse_number(operand);
            /* Update this line's address to the new LC */
            result->lines[result->line_count - 1].address = lc;
        } else if (strcmp(mnemonic, "END") == 0) {
            break;  /* Stop processing */
        } else if (strcmp(mnemonic, "DB") == 0) {
            lc += 1;  /* 1 byte per DB */
        } else if (strcmp(mnemonic, "DW") == 0) {
            lc += 2;  /* 2 bytes per DW */
        } else {
            /* Look up instruction size in opcode table */
            OpcodeEntry *entry = lookup_opcode(mnemonic);
            if (entry == NULL) {
                fprintf(stderr, "Error (line %d): Unknown mnemonic '%s'\n",
                        line_no, mnemonic);
                error = 1;
            } else {
                lc += entry->size;
            }
        }
    }

    fclose(fp);
    return error ? -1 : 0;
}
