#include <stdio.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    char lhs;
    char rhs[20];
} Prod;

char nt[] = {'E', 'A', 'T', 'B', 'F'};      // A = E', B = T'
char t[]  = {'i', '+', '*', '(', ')', '$'}; // i = id
Prod p[] = {
    {'E', "TA"}, {'A', "+TA"}, {'A', "e"}, {'T', "FB"},
    {'B', "*FB"}, {'B', "e"}, {'F', "i"}, {'F', "(E)"}
};

#define NNT ((int)(sizeof(nt) / sizeof(nt[0])))
#define NTM ((int)(sizeof(t) / sizeof(t[0])))
#define NPR ((int)(sizeof(p) / sizeof(p[0])))
#define SZ 20
#define MAX 200

char first[NNT][SZ], follow[NNT][SZ], table[NNT][NTM][SZ];

int has(char s[], char c) {
    for (int i = 0; s[i]; i++) if (s[i] == c) return 1;
    return 0;
}

int add(char s[], char c) {
    if (!c || has(s, c)) return 0;
    int n = strlen(s);
    s[n] = c;
    s[n + 1] = '\0';
    return 1;
}

int merge(char dst[], char src[], char skip) {
    int changed = 0;
    for (int i = 0; src[i]; i++) if (src[i] != skip) changed |= add(dst, src[i]);
    return changed;
}

int idx(char arr[], int n, char c) {
    for (int i = 0; i < n; i++) if (arr[i] == c) return i;
    return -1;
}

int nt_idx(char c) { return idx(nt, NNT, c); }
int t_idx(char c) { return idx(t, NTM, c); }
int is_terminal(char c) { return t_idx(c) != -1; }

void first_of_str(char s[], char out[]) {
    out[0] = '\0';
    if (!s[0] || (s[0] == 'e' && !s[1])) { add(out, 'e'); return; }

    for (int i = 0; s[i]; i++) {
        if (is_terminal(s[i])) { add(out, s[i]); return; }
        int ni = nt_idx(s[i]);
        if (ni == -1) return;
        merge(out, first[ni], 'e');
        if (!has(first[ni], 'e')) return;
    }
    add(out, 'e');
}

void compute_first() {
    for (int i = 0; i < NNT; i++) first[i][0] = '\0';

    int changed = 1;
    while (changed) {
        changed = 0;
        for (int i = 0; i < NPR; i++) {
            int a = nt_idx(p[i].lhs);
            char f[SZ];
            first_of_str(p[i].rhs, f);
            changed |= merge(first[a], f, '\0');
        }
    }
}

void compute_follow() {
    for (int i = 0; i < NNT; i++) follow[i][0] = '\0';
    add(follow[nt_idx('E')], '$');

    int changed = 1;
    while (changed) {
        changed = 0;
        for (int i = 0; i < NPR; i++) {
            int a = nt_idx(p[i].lhs);
            for (int j = 0; p[i].rhs[j]; j++) {
                int b = nt_idx(p[i].rhs[j]);
                if (b == -1) continue;

                char fs[SZ];
                first_of_str(p[i].rhs + j + 1, fs);
                changed |= merge(follow[b], fs, 'e');
                if (has(fs, 'e')) changed |= merge(follow[b], follow[a], '\0');
            }
        }
    }
}

void build_table() {
    for (int i = 0; i < NNT; i++)
        for (int j = 0; j < NTM; j++) strcpy(table[i][j], "-");

    for (int i = 0; i < NPR; i++) {
        int a = nt_idx(p[i].lhs);
        char f[SZ];
        first_of_str(p[i].rhs, f);

        for (int j = 0; f[j]; j++) {
            if (f[j] == 'e') continue;
            int c = t_idx(f[j]);
            if (c != -1) strcpy(table[a][c], p[i].rhs);
        }

        if (has(f, 'e')) {
            for (int j = 0; follow[a][j]; j++) {
                int c = t_idx(follow[a][j]);
                if (c != -1) strcpy(table[a][c], "e");
            }
        }
    }
}

int normalize(char raw[], char out[]) {
    int i = 0, k = 0;
    while (raw[i] && raw[i] != '\n') {
        if (isspace((unsigned char)raw[i])) { i++; continue; }
        if (raw[i] == 'i' && raw[i + 1] == 'd') { out[k++] = 'i'; i += 2; continue; }
        if (raw[i] == '+' || raw[i] == '*' || raw[i] == '(' || raw[i] == ')') { out[k++] = raw[i++]; continue; }
        return 0;
    }
    out[k++] = '$';
    out[k] = '\0';
    return 1;
}

int parse(char input[]) {
    char st[MAX];
    int top = -1, ip = 0;
    st[++top] = '$';
    st[++top] = 'E';

    while (top >= 0) {
        char X = st[top], a = input[ip];
        if (X == '$' && a == '$') return 1;

        if (is_terminal(X)) {
            if (X != a) return 0;
            top--;
            ip++;
            continue;
        }

        int r = nt_idx(X), c = t_idx(a);
        if (r == -1 || c == -1 || strcmp(table[r][c], "-") == 0) return 0;

        top--;
        if (strcmp(table[r][c], "e") != 0)
            for (int i = (int)strlen(table[r][c]) - 1; i >= 0; i--) st[++top] = table[r][c][i];
    }
    return 0;
}

void print_table() {
    printf("\nLL(1) Parse Table (A=E', B=T'):\n\n      ");
    for (int i = 0; i < NTM; i++) printf("%-7c ", t[i]);
    printf("\n");
    for (int i = 0; i < NNT; i++) {
        printf("%c   ", nt[i]);
        for (int j = 0; j < NTM; j++) printf("%-7s ", table[i][j]);
        printf("\n");
    }
}

int main() {
    char raw[MAX], input[MAX];

    compute_first();
    compute_follow();
    build_table();
    print_table();

    printf("\nEnter input string (use id, +, *, (, )): ");
    fgets(raw, sizeof(raw), stdin);

    if (!normalize(raw, input)) {
        printf("Invalid token in input!\n");
        return 0;
    }

    printf(parse(input) ? "Accepted\n" : "Rejected\n");
    return 0;
}
