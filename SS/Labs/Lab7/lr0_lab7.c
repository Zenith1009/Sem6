#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define STATES 7
#define TERMS 3      /* a, b, $ */
#define NONTERMS 2   /* E, T */
#define MAX_STACK 256

/* Productions:
   (1) E -> T T
   (2) T -> a T
   (3) T -> b
*/
static const char lhs[] = {'?', 'E', 'T', 'T'};
static const int rhs_len[] = {0, 2, 2, 1};
static const char *prod_text[] = {
    "",
    "E -> T T",
    "T -> a T",
    "T -> b"
};

/* LR(0) ACTION table encoded as strings: sX, rY, acc, - */
static const char *action[STATES][TERMS] = {
    {"s3", "s4", "-"},
    {"-", "-", "acc"},
    {"s3", "s4", "-"},
    {"s3", "s4", "-"},
    {"r3", "r3", "r3"},
    {"r1", "r1", "r1"},
    {"r2", "r2", "r2"}
};

/* GOTO[E, T] */
static const int gotos[STATES][NONTERMS] = {
    {1, 2},
    {-1, -1},
    {-1, 5},
    {-1, 6},
    {-1, -1},
    {-1, -1},
    {-1, -1}
};

static int term_index(char c) {
    if (c == 'a') return 0;
    if (c == 'b') return 1;
    if (c == '$' || c == '\0') return 2;
    return -1;
}

static int nonterm_index(char c) {
    if (c == 'E') return 0;
    if (c == 'T') return 1;
    return -1;
}

static void print_table(void) {
    int i;
    printf("\nLR(0) Parse Table\n");
    printf("State |   a   b   $  ||  E   T\n");
    printf("--------------------------------\n");
    for (i = 0; i < STATES; i++) {
        printf("  %d   | %-3s %-3s %-3s || ", i, action[i][0], action[i][1], action[i][2]);
        if (gotos[i][0] >= 0) printf("%-3d ", gotos[i][0]); else printf("-   ");
        if (gotos[i][1] >= 0) printf("%-3d", gotos[i][1]); else printf("-  ");
        printf("\n");
    }
}

static void print_stack(const int st[], const char sym[], int top, char *out, size_t n) {
    size_t used = 0;
    int i;
    used += snprintf(out + used, n - used, "%d", st[0]);
    for (i = 1; i <= top && used < n; i++) {
        used += snprintf(out + used, n - used, " %c %d", sym[i], st[i]);
    }
}

static int parse(const char *raw) {
    char input[256];
    int st[MAX_STACK];
    char sym[MAX_STACK];
    int top = 0;
    int ip = 0;
    int step = 1;

    strncpy(input, raw, sizeof(input) - 2);
    input[sizeof(input) - 2] = '\0';
    strcat(input, "$");

    st[0] = 0;
    sym[0] = '#';

    printf("\nParser Moves (LR(0)) for input \"%s\"\n", raw);
    printf("Step | Stack                     | Input     | Action\n");
    printf("-----------------------------------------------------------\n");

    while (1) {
        int state = st[top];
        int ti = term_index(input[ip]);
        char stack_view[256];
        const char *act;

        if (ti < 0) {
            print_stack(st, sym, top, stack_view, sizeof(stack_view));
            printf("%-4d | %-25s | %-9s | error (invalid symbol)\n", step, stack_view, input + ip);
            return 0;
        }

        act = action[state][ti];
        print_stack(st, sym, top, stack_view, sizeof(stack_view));

        if (act[0] == 's') {
            int next = atoi(act + 1);
            printf("%-4d | %-25s | %-9s | shift %d\n", step, stack_view, input + ip, next);
            if (top + 1 >= MAX_STACK) return 0;
            top++;
            sym[top] = input[ip++];
            st[top] = next;
        } else if (act[0] == 'r') {
            int p = atoi(act + 1);
            int pop_count = rhs_len[p];
            int base_state;
            int g;
            printf("%-4d | %-25s | %-9s | reduce %s\n", step, stack_view, input + ip, prod_text[p]);
            if (top - pop_count < 0) return 0;
            top -= pop_count;
            base_state = st[top];
            g = gotos[base_state][nonterm_index(lhs[p])];
            if (g < 0 || top + 1 >= MAX_STACK) return 0;
            top++;
            sym[top] = lhs[p];
            st[top] = g;
        } else if (strcmp(act, "acc") == 0) {
            printf("%-4d | %-25s | %-9s | accept\n", step, stack_view, input + ip);
            return 1;
        } else {
            printf("%-4d | %-25s | %-9s | error\n", step, stack_view, input + ip);
            return 0;
        }

        step++;
    }
}

int main(void) {
    char input[256];

    printf("Grammar:\n");
    printf("E -> T T\n");
    printf("T -> a T | b\n");

    print_table();

    printf("\nEnter input string over {a,b}: ");
    if (!fgets(input, sizeof(input), stdin)) return 0;

    if (strlen(input) > 0 && input[strlen(input) - 1] == '\n') {
        input[strlen(input) - 1] = '\0';
    }

    printf("\nResult: %s\n", parse(input) ? "Accepted" : "Rejected");
    return 0;
}
