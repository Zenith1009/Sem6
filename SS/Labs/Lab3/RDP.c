#include <stdio.h>
#include <string.h>
#include <ctype.h>

char input[100];
int pos = 0;
int error = 0;

void E();
void E_prime();
void T();
void T_prime();
void F();

void skip_space() {
    while (input[pos] == ' ' || input[pos] == '\t')
        pos++;
}

void match(char c) {
    skip_space();
    if (input[pos] == c)
        pos++;
    else
        error = 1;
}

// E -> T E'
void E() {
    if (error) return;
    T();
    E_prime();
}

// E' -> + T E' | eps
void E_prime() {
    if (error) return;
    skip_space();
    if (input[pos] == '+') {
        pos++;
        T();
        E_prime();
    }
    // else epsilon, do nothing
}

// T -> F T'
void T() {
    if (error) return;
    F();
    T_prime();
}

// T' -> * F T' | epsilon
void T_prime() {
    if (error) return;
    skip_space();
    if (input[pos] == '*') {
        pos++;
        F();
        T_prime();
    }
    // else epsilon, do nothing
}

// F -> ( E ) | id
void F() {
    if (error) return;
    skip_space();
    
    // Check for ( E )
    if (input[pos] == '(') {
        pos++;
        E();
        match(')');
    }
    // Check for id (identifier - letter followed by alphanumeric)
    else if (isalpha(input[pos])) {
        while (isalnum(input[pos]))
            pos++;
    }
    // Check for number
    else if (isdigit(input[pos])) {
        while (isdigit(input[pos]))
            pos++;
    }
    else {
        error = 1;
    }
}

int main() {
    printf("Enter expression: ");
    fgets(input, sizeof(input), stdin);
    input[strlen(input)-1] = '\0';  // remove newline
    
    printf("\nGrammar (after left recursion elimination):\n");
    printf("E  -> T E'\n");
    printf("E' -> + T E' | epsilon\n");
    printf("T  -> F T'\n");
    printf("T' -> * F T' | epsilon\n");
    printf("F  -> ( E ) | id\n\n");
    E();
    skip_space();
    printf("Result: ");
    if (!error && input[pos] == '\0')
        printf("VALID expression (Accepted)\n");
    else
        printf("INVALID expression (Rejected)\n");
    return 0;
}
