/*
 * utils.c
 * Helper functions for the 2-Pass 8085 Assembler
 */

#include "assembler.h"
#include "utils.h"

/* Remove leading and trailing whitespace in-place */
void str_trim(char *s) {
    int i, start = 0, end = (int)strlen(s) - 1;

    /* Find first non-space */
    while (s[start] && isspace((unsigned char)s[start]))
        start++;

    /* Find last non-space */
    while (end > start && isspace((unsigned char)s[end]))
        end--;

    int len = end - start + 1;
    if (len <= 0) { s[0] = '\0'; return; }

    for (i = 0; i < len; i++)
        s[i] = s[start + i];
    s[len] = '\0';
}

/* Convert string to uppercase in-place */
void str_upper(char *s) {
    while (*s) {
        *s = (char)toupper((unsigned char)*s);
        s++;
    }
}

/*
 * Strip inline/full-line comments (everything after ';')
 * Also trims trailing whitespace after stripping.
 */
void strip_comment(char *s) {
    char *p = strchr(s, ';');
    if (p) *p = '\0';
    str_trim(s);
}

/*
 * parse_number: parse a number literal.
 * Supports:
 *   - Hex with 'H' suffix: e.g. 2000H, 0FFH
 *   - Hex with '0x' prefix: e.g. 0x2000
 *   - Decimal: e.g. 100
 * Returns the integer value.
 */
int parse_number(const char *s) {
    char buf[30];
    int  len;

    strncpy(buf, s, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';
    str_upper(buf);
    len = (int)strlen(buf);

    /* Hex with H suffix */
    if (len > 0 && buf[len - 1] == 'H') {
        buf[len - 1] = '\0';
        return (int)strtol(buf, NULL, 16);
    }
    /* Hex with 0x prefix */
    if (len > 2 && buf[0] == '0' && buf[1] == 'X') {
        return (int)strtol(buf + 2, NULL, 16);
    }
    /* Decimal */
    return (int)strtol(buf, NULL, 10);
}

/*
 * is_valid_label: returns 1 if s is a valid label name.
 * Labels must start with a letter and contain only alphanumeric chars + '_'.
 * Max length: MAX_LABEL_LEN - 1.
 */
int is_valid_label(const char *s) {
    int i;
    if (!s || !*s) return 0;
    if (!isalpha((unsigned char)s[0])) return 0;
    for (i = 1; s[i] != '\0'; i++) {
        if (!isalnum((unsigned char)s[i]) && s[i] != '_')
            return 0;
    }
    return (i < 20);
}

/*
 * split_operands: split "op1, op2" into op1 and op2 (by comma).
 * op1 and op2 must be pre-allocated buffers of at least MAX_OPERAND chars.
 * If there is no comma, op1 gets the full string and op2 is empty.
 */
void split_operands(const char *operand, char *op1, char *op2) {
    char buf[MAX_OPERAND];
    char *comma;

    strncpy(buf, operand, MAX_OPERAND - 1);
    buf[MAX_OPERAND - 1] = '\0';

    comma = strchr(buf, ',');
    if (comma) {
        *comma = '\0';
        strncpy(op1, buf, MAX_OPERAND - 1);
        op1[MAX_OPERAND - 1] = '\0';
        strncpy(op2, comma + 1, MAX_OPERAND - 1);
        op2[MAX_OPERAND - 1] = '\0';
        str_trim(op1);
        str_trim(op2);
    } else {
        strncpy(op1, buf, MAX_OPERAND - 1);
        op1[MAX_OPERAND - 1] = '\0';
        str_trim(op1);
        op2[0] = '\0';
    }
}
