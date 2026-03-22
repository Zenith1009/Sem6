#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_NT 10
#define MAX_PROD 20
#define MAX_RHS 20

typedef struct {
    char lhs;
    char rhs[MAX_RHS];
} Production;

/* Use # for epsilon */
static Production prods[] = {
    {'S', "aBDh"},
    {'B', "cC"},
    {'C', "bC"},
    {'C', "#"},
    {'D', "EF"},
    {'E', "g"},
    {'E', "#"},
    {'F', "f"},
    {'F', "#"}
};

static const int P = sizeof(prods) / sizeof(prods[0]);
static const char nonterms[] = {'S', 'B', 'C', 'D', 'E', 'F'};
static const int N = sizeof(nonterms) / sizeof(nonterms[0]);

static int nt_index(char nt) {
    int i;
    for (i = 0; i < N; i++) {
        if (nonterms[i] == nt) return i;
    }
    return -1;
}

static int add_to_set(int set[128], char c) {
    unsigned char uc = (unsigned char)c;
    if (!set[uc]) {
        set[uc] = 1;
        return 1;
    }
    return 0;
}

static int union_set(int dest[128], const int src[128], int skip_epsilon) {
    int changed = 0;
    int i;
    for (i = 0; i < 128; i++) {
        if (!src[i]) continue;
        if (skip_epsilon && i == '#') continue;
        if (!dest[i]) {
            dest[i] = 1;
            changed = 1;
        }
    }
    return changed;
}

/* FIRST sets for non-terminals */
static int first_nt[MAX_NT][128];
/* FOLLOW sets for non-terminals */
static int follow_nt[MAX_NT][128];

static void first_of_string(const char *str, int out[128]) {
    int i;
    int all_can_be_epsilon = 1;
    memset(out, 0, 128 * sizeof(int));

    if (str[0] == '\0') {
        out['#'] = 1;
        return;
    }

    for (i = 0; str[i] != '\0'; i++) {
        char sym = str[i];

        if (!isupper((unsigned char)sym)) {
            add_to_set(out, sym);
            all_can_be_epsilon = 0;
            break;
        } else {
            int idx = nt_index(sym);
            if (idx < 0) {
                all_can_be_epsilon = 0;
                break;
            }

            union_set(out, first_nt[idx], 1);
            if (!first_nt[idx]['#']) {
                all_can_be_epsilon = 0;
                break;
            }
        }
    }

    if (all_can_be_epsilon) {
        add_to_set(out, '#');
    }
}

static void compute_first_sets(void) {
    int changed = 1;
    while (changed) {
        int i;
        changed = 0;

        for (i = 0; i < P; i++) {
            int lhs_i = nt_index(prods[i].lhs);
            int f[128];

            first_of_string(prods[i].rhs, f);
            if (union_set(first_nt[lhs_i], f, 0)) {
                changed = 1;
            }
        }
    }
}

static void compute_follow_sets(void) {
    int changed = 1;

    /* Start symbol: S */
    add_to_set(follow_nt[nt_index('S')], '$');

    while (changed) {
        int i;
        changed = 0;

        for (i = 0; i < P; i++) {
            int lhs_i = nt_index(prods[i].lhs);
            const char *rhs = prods[i].rhs;
            int j;

            for (j = 0; rhs[j] != '\0'; j++) {
                char B = rhs[j];
                int b_i;

                if (!isupper((unsigned char)B)) continue;
                b_i = nt_index(B);

                if (rhs[j + 1] != '\0') {
                    int first_beta[128];
                    first_of_string(rhs + j + 1, first_beta);

                    if (union_set(follow_nt[b_i], first_beta, 1)) {
                        changed = 1;
                    }
                    if (first_beta['#']) {
                        if (union_set(follow_nt[b_i], follow_nt[lhs_i], 0)) {
                            changed = 1;
                        }
                    }
                } else {
                    if (union_set(follow_nt[b_i], follow_nt[lhs_i], 0)) {
                        changed = 1;
                    }
                }
            }
        }
    }
}

static void print_set(const int set[128]) {
    int first = 1;
    int c;
    printf("{ ");
    for (c = 0; c < 128; c++) {
        if (!set[c]) continue;
        if (!first) printf(", ");
        printf("%c", c);
        first = 0;
    }
    printf(" }");
}

static int terminals[128];
static char term_list[32];
static int T = 0;

static void collect_terminals(void) {
    int i, j;
    memset(terminals, 0, sizeof(terminals));

    for (i = 0; i < P; i++) {
        for (j = 0; prods[i].rhs[j] != '\0'; j++) {
            char c = prods[i].rhs[j];
            if (!isupper((unsigned char)c) && c != '#') {
                terminals[(unsigned char)c] = 1;
            }
        }
    }
    terminals[(unsigned char)'$'] = 1;

    T = 0;
    for (i = 0; i < 128; i++) {
        if (terminals[i]) {
            term_list[T++] = (char)i;
        }
    }
}

static int table_prod[MAX_NT][128];

static void build_ll1_table(int *is_ll1) {
    int i, j;
    *is_ll1 = 1;

    for (i = 0; i < MAX_NT; i++) {
        for (j = 0; j < 128; j++) {
            table_prod[i][j] = -1;
        }
    }

    for (i = 0; i < P; i++) {
        int a_i = nt_index(prods[i].lhs);
        int first_alpha[128];
        first_of_string(prods[i].rhs, first_alpha);

        for (j = 0; j < 128; j++) {
            if (j == '#') continue;
            if (!first_alpha[j]) continue;

            if (table_prod[a_i][j] != -1 && table_prod[a_i][j] != i) {
                *is_ll1 = 0;
            }
            table_prod[a_i][j] = i;
        }

        if (first_alpha['#']) {
            int c;
            for (c = 0; c < 128; c++) {
                if (!follow_nt[a_i][c]) continue;
                if (table_prod[a_i][c] != -1 && table_prod[a_i][c] != i) {
                    *is_ll1 = 0;
                }
                table_prod[a_i][c] = i;
            }
        }
    }
}

static void print_table(void) {
    int i, j;
    printf("\nLL(1) Parsing Table\n\n");
    printf("NT/T\t");
    for (j = 0; j < T; j++) {
        printf("%c\t", term_list[j]);
    }
    printf("\n");

    for (i = 0; i < N; i++) {
        printf("%c\t", nonterms[i]);
        for (j = 0; j < T; j++) {
            int p = table_prod[i][(unsigned char)term_list[j]];
            if (p == -1) {
                printf("-\t");
            } else {
                printf("%c->%s\t", prods[p].lhs, prods[p].rhs);
            }
        }
        printf("\n");
    }
}

int main(void) {
    int i;
    int is_ll1;

    printf("Given Grammar:\n");
    printf("S -> aBDh\n");
    printf("B -> cC\n");
    printf("C -> bC | #\n");
    printf("D -> EF\n");
    printf("E -> g | #\n");
    printf("F -> f | #\n");

    compute_first_sets();
    compute_follow_sets();
    collect_terminals();
    build_ll1_table(&is_ll1);

    printf("\nFIRST Sets:\n");
    for (i = 0; i < N; i++) {
        printf("FIRST(%c) = ", nonterms[i]);
        print_set(first_nt[i]);
        printf("\n");
    }

    printf("\nFOLLOW Sets:\n");
    for (i = 0; i < N; i++) {
        printf("FOLLOW(%c) = ", nonterms[i]);
        print_set(follow_nt[i]);
        printf("\n");
    }

    print_table();

    printf("\nGrammar status: %s\n", is_ll1 ? "Grammar is LL(1)." : "Grammar is NOT LL(1). (Conflict found)");
    return 0;
}
