#include <stdio.h>
#include <string.h>

#define MAX 128

typedef struct {
    int from;
    char sym;
    int to;
} Transition;

Transition T[MAX];
int tcount = 0;
int final_state = 0;

void add_tr(int from, char sym, int to) {
    T[tcount].from = from;
    T[tcount].sym = sym;
    T[tcount].to = to;
    tcount++;
}

void build_dfa(const char *re) {
    int cur = 0;
    tcount = 0;
    int n = (int)strlen(re);

    for (int i = 0; i < n; ++i) {
        char ch = re[i];
        char nxt = (i + 1 < n) ? re[i + 1] : '\0';

        if (ch == '*' || ch == '+' || ch == '|') continue;

        if (nxt == '*') {
            add_tr(cur, ch, cur);
            i++;
        } else if (nxt == '+') {
            add_tr(cur, ch, cur + 1);
            add_tr(cur + 1, ch, cur + 1);
            cur += 1;
            i++;
        } else {
            add_tr(cur, ch, cur + 1);
            cur += 1;
        }
    }
    final_state = cur;
}

int validate(const char *s) {
    int state = 0;
    for (int i = 0; s[i]; ++i) {
        char ch = s[i];
        int moved = 0;
        for (int j = 0; j < tcount; ++j) {
            if (T[j].from == state && T[j].sym == ch) {
                state = T[j].to;
                moved = 1;
                break;
            }
        }
        if (!moved) return 0;
    }
    return state == final_state;
}

void print_dfa(void) {
    printf("\nDFA\n");
    printf("%-8s %-8s %-8s\n", "State", "Input", "Next");
    printf("------------------------\n");
    for (int i = 0; i < tcount; ++i) {
        printf("q%-7d %-8c q%-7d\n", T[i].from, T[i].sym, T[i].to);
    }
    printf("------------------------\n");
    printf("Start: q0\nFinal: q%d\n", final_state);
}

int main() {
    char re[64], s[64], c;
    printf("Enter regex: ");
    scanf("%63s", re);

    build_dfa(re);
    print_dfa();

    do {
        printf("\nTest a string? (y/n): ");
        scanf(" %c", &c);
        if (c == 'y' || c == 'Y') {
            printf("String: ");
            scanf("%63s", s);
            if (validate(s)) printf("ACCEPTED\n");
            else printf("REJECTED\n");
        }
    } while (c == 'y' || c == 'Y');
    return 0;
}