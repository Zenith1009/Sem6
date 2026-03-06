#include <stdio.h>
#include <string.h>

#define MAX 10

char productions[MAX][MAX];
char first[MAX], follow[MAX];
int f_count = 0, fo_count = 0;

void add_first(char c) {
    for (int i = 0; i < f_count; i++) {
        if (first[i] == c) return;
    }
    first[f_count++] = c;
}

void add_follow(char c) {
    if (c == 'e') return;
    for (int i = 0; i < fo_count; i++) {
        if (follow[i] == c) return;
    }
    follow[fo_count++] = c;
}

int main() {
    printf("\nGrammar A:\n");
    printf("S -> aSbS | bSaS | e\n\n");
    
    // FIRST calculation
    add_first('a');
    add_first('b');
    add_first('e');
    
    printf("FIRST(S) = { ");
    for (int i = 0; i < f_count; i++) {
        if (first[i] == 'e')
            printf("ε");
        else
            printf("%c", first[i]);
        if (i < f_count - 1) printf(", ");
    }
    printf(" }\n\n");
    
    // FOLLOW calculation
    add_follow('$');
    add_follow('a');
    add_follow('b');
    
    printf("FOLLOW(S) = { ");
    for (int i = 0; i < fo_count; i++) {
        printf("%c", follow[i]);
        if (i < fo_count - 1) printf(", ");
    }
    printf(" }\n\n");
    
    return 0;
}
