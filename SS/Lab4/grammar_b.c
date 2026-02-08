#include <stdio.h>
#include <string.h>

char first_E[10], first_E_prime[10], first_T[10], first_T_prime[10], first_F[10];
char follow_E[10], follow_E_prime[10], follow_T[10], follow_T_prime[10], follow_F[10];
int f_E = 0, f_Ep = 0, f_T = 0, f_Tp = 0, f_F = 0;
int fo_E = 0, fo_Ep = 0, fo_T = 0, fo_Tp = 0, fo_F = 0;

void add_to_first(char *set, int *count, char c) {
    for (int i = 0; i < *count; i++) {
        if (set[i] == c) return;
    }
    set[(*count)++] = c;
}

void add_to_follow(char *set, int *count, char c) {
    if (c == 'e') return;
    for (int i = 0; i < *count; i++) {
        if (set[i] == c) return;
    }
    set[(*count)++] = c;
}

void compute_first() {
    // FIRST(F) = { (, id }
    add_to_first(first_F, &f_F, '(');
    add_to_first(first_F, &f_F, 'i');
    
    // FIRST(T') = { *, e }
    add_to_first(first_T_prime, &f_Tp, '*');
    add_to_first(first_T_prime, &f_Tp, 'e');
    
    // FIRST(T) = FIRST(F) = { (, id }
    add_to_first(first_T, &f_T, '(');
    add_to_first(first_T, &f_T, 'i');
    
    // FIRST(E') = { +, e }
    add_to_first(first_E_prime, &f_Ep, '+');
    add_to_first(first_E_prime, &f_Ep, 'e');
    
    // FIRST(E) = FIRST(T) = { (, id }
    add_to_first(first_E, &f_E, '(');
    add_to_first(first_E, &f_E, 'i');
}

void compute_follow() {
    // FOLLOW(E) = { $, ) }
    add_to_follow(follow_E, &fo_E, '$');
    add_to_follow(follow_E, &fo_E, ')');
    
    // FOLLOW(E') = FOLLOW(E) = { $, ) }
    add_to_follow(follow_E_prime, &fo_Ep, '$');
    add_to_follow(follow_E_prime, &fo_Ep, ')');
    
    // FOLLOW(T) = FIRST(E') - {e} U FOLLOW(E) = { +, $, ) }
    add_to_follow(follow_T, &fo_T, '+');
    add_to_follow(follow_T, &fo_T, '$');
    add_to_follow(follow_T, &fo_T, ')');
    
    // FOLLOW(T') = FOLLOW(T) = { +, $, ) }
    add_to_follow(follow_T_prime, &fo_Tp, '+');
    add_to_follow(follow_T_prime, &fo_Tp, '$');
    add_to_follow(follow_T_prime, &fo_Tp, ')');
    
    // FOLLOW(F) = FIRST(T') - {e} U FOLLOW(T) = { *, +, $, ) }
    add_to_follow(follow_F, &fo_F, '*');
    add_to_follow(follow_F, &fo_F, '+');
    add_to_follow(follow_F, &fo_F, '$');
    add_to_follow(follow_F, &fo_F, ')');
}

void print_first() {
    printf("\nFIRST SETS:\n");
    
    printf("FIRST(E) = { ");
    for (int i = 0; i < f_E; i++) {
        if (first_E[i] == 'i') printf("id");
        else printf("%c", first_E[i]);
        if (i < f_E - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FIRST(E') = { ");
    for (int i = 0; i < f_Ep; i++) {
        if (first_E_prime[i] == 'e') printf("ε");
        else printf("%c", first_E_prime[i]);
        if (i < f_Ep - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FIRST(T) = { ");
    for (int i = 0; i < f_T; i++) {
        if (first_T[i] == 'i') printf("id");
        else printf("%c", first_T[i]);
        if (i < f_T - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FIRST(T') = { ");
    for (int i = 0; i < f_Tp; i++) {
        if (first_T_prime[i] == 'e') printf("ε");
        else printf("%c", first_T_prime[i]);
        if (i < f_Tp - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FIRST(F) = { ");
    for (int i = 0; i < f_F; i++) {
        if (first_F[i] == 'i') printf("id");
        else printf("%c", first_F[i]);
        if (i < f_F - 1) printf(", ");
    }
    printf(" }\n");
}

void print_follow() {
    printf("\nFOLLOW SETS:\n");
    
    printf("FOLLOW(E) = { ");
    for (int i = 0; i < fo_E; i++) {
        printf("%c", follow_E[i]);
        if (i < fo_E - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FOLLOW(E') = { ");
    for (int i = 0; i < fo_Ep; i++) {
        printf("%c", follow_E_prime[i]);
        if (i < fo_Ep - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FOLLOW(T) = { ");
    for (int i = 0; i < fo_T; i++) {
        printf("%c", follow_T[i]);
        if (i < fo_T - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FOLLOW(T') = { ");
    for (int i = 0; i < fo_Tp; i++) {
        printf("%c", follow_T_prime[i]);
        if (i < fo_Tp - 1) printf(", ");
    }
    printf(" }\n");
    
    printf("FOLLOW(F) = { ");
    for (int i = 0; i < fo_F; i++) {
        printf("%c", follow_F[i]);
        if (i < fo_F - 1) printf(", ");
    }
    printf(" }\n");
}

int main() {
    printf("\nGrammar B:\n");
    printf("E  -> T E'\n");
    printf("E' -> +T E' | e\n");
    printf("T  -> F T'\n");
    printf("T' -> *F T' | e\n");
    printf("F  -> (E) | id\n");
    
    compute_first();
    compute_follow();
    
    print_first();
    print_follow();
    
    printf("\n");
    return 0;
}
