// Program to recognize arithmetic expression and identify identifiers & operators
#include <stdio.h>
#include <string.h>
#include <ctype.h>

char identifiers[20][20];
char operators[20];
int id_count = 0, op_count = 0;

int main() {
    char expr[100];
    char token[20];
    int i, j, valid = 1;
    
    printf("Enter arithmetic expression: ");
    fgets(expr, sizeof(expr), stdin);
    expr[strlen(expr)-1] = '\0';  // remove newline
    
    for (i = 0; expr[i] != '\0'; i++) {
        // Skip spaces
        if (expr[i] == ' ' || expr[i] == '\n')
            continue;
        
        // Check for operators
        if (expr[i] == '+' || expr[i] == '-' || expr[i] == '*' || 
            expr[i] == '/' || expr[i] == '%') {
            operators[op_count] = expr[i];
            op_count++;
        }
        // Check for identifiers (starts with letter)
        else if (isalpha(expr[i])) {
            j = 0;
            while (isalnum(expr[i])) {
                token[j] = expr[i];
                j++;
                i++;
            }
            token[j] = '\0';
            i--;  // adjust for loop increment
            strcpy(identifiers[id_count], token);
            id_count++;
        }
        // Skip numbers
        else if (isdigit(expr[i])) {
            while (isdigit(expr[i]))
                i++;
            i--;
        }
        // Skip parentheses
        else if (expr[i] == '(' || expr[i] == ')') {
            continue;
        }
        else {
            valid = 0;
            break;
        }
    }
    
    if (valid) {
        printf("\nVALID arithmetic expression\n");
        
        printf("\nIdentifiers: ");
        for (i = 0; i < id_count; i++)
            printf("%s ", identifiers[i]);
        
        printf("\nOperators: ");
        for (i = 0; i < op_count; i++)
            printf("%c ", operators[i]);
        printf("\n");
    }
    else {
        printf("\nINVALID expression\n");
    }
    
    return 0;
}
