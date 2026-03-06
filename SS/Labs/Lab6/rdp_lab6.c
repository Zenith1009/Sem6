#include <stdio.h>
#include <string.h>
#include <ctype.h>

char input[200];
int pos = 0;
int error = 0;

void E();
void Eprime();
void T();
void Tprime();
void F();

void skip_space() {
    while (input[pos] == ' ' || input[pos] == '\t')
        pos++;
}

void E() {
    if (error) return;
    T();
    Eprime();
}

void Eprime() {
    if (error) return;
    skip_space();
    if (input[pos] == '+') {
        pos++;
        T();
        Eprime();
    }
}

void T() {
    if (error) return;
    F();
    Tprime();
}

void Tprime() {
    if (error) return;
    skip_space();
    if (input[pos] == '*') {
        pos++;
        F();
        Tprime();
    }
}

void F() {
    if (error) return;
    skip_space();

    if (input[pos] == '(') {
        pos++;
        E();
        skip_space();
        if (input[pos] == ')')
            pos++;
        else
            error = 1;
    }
    else if (isalpha((unsigned char)input[pos])) {
        while (isalnum((unsigned char)input[pos]))
            pos++;
    }
    else {
        error = 1;
    }
}

int main() {
    printf("Grammar:\n");
    printf("E  -> T E'\n");
    printf("E' -> + T E' | @\n");
    printf("T  -> F T'\n");
    printf("T' -> * F T' | @\n");
    printf("F  -> id | (E)\n\n");

    printf("Enter string: ");
    fgets(input, sizeof(input), stdin);

    if (strlen(input) > 0 && input[strlen(input) - 1] == '\n')
        input[strlen(input) - 1] = '\0';

    E();
    skip_space();

    if (!error && input[pos] == '\0')
        printf("Accepted\n");
    else
        printf("Rejected\n");

    return 0;
}
