#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isKeyword(char str[]) {
    char keywords[12][10] = {"int", "float", "if", "else", "while",
                             "for", "return", "void", "char", "main",
                             "printf", "scanf"};
    for(int i = 0; i < 12; i++) {
        if(strcmp(keywords[i], str) == 0)
            return 1;
    }
    return 0;
}

int main() {
    char input[100], token[20];
    int i = 0, j = 0;
    
    printf("Enter a C statement: ");
    fgets(input, 100, stdin);
    
    printf("\nTokens identified:\n");
    printf("-------------------\n");
    
    while(input[i] != '\0') {
        j = 0;
        
        if(input[i] == '"') {
            i++; // used to only consider the string without the quotes
            while(input[i] != '\0' && input[i] != '"') {
                token[j++] = input[i++];
            }
            token[j] = '\0';
            if(input[i] == '"') i++; // skip closing quote
            printf("String Literal: %s\n", token);
        }
        else if(isalpha(input[i]) || input[i] == '_') {
            while(isalnum(input[i])) {
                token[j++] = input[i++];
            }
            token[j] = '\0';
            
            if(isKeyword(token))
                printf("Keyword: %s\n", token);
            else
                printf("Identifier: %s\n", token);
        }
        else if(isdigit(input[i])) {
            while(isdigit(input[i])) {
                token[j++] = input[i++];
            }
            token[j] = '\0';
            printf("Number: %s\n", token);
        }
        else if((input[i] == '>' && input[i+1] == '=') ||
                (input[i] == '<' && input[i+1] == '=') ||
                (input[i] == '=' && input[i+1] == '=') ||
                (input[i] == '!' && input[i+1] == '=')) {
            printf("Operator: %c%c\n", input[i], input[i+1]);
            i += 2;
        }
        else if(input[i] == '+' || input[i] == '-' || input[i] == '*' || 
                input[i] == '/' || input[i] == '=' || input[i] == '<' ||
                input[i] == '>') {
            printf("Operator: %c\n", input[i]);
            i++;
        }
        else if(input[i] == ';' || input[i] == ',' || input[i] == '(' || 
                input[i] == ')' || input[i] == '{' || input[i] == '}') {
            printf("Special Symbol: %c\n", input[i]);
            i++;
        }
        else {
            i++;
        }
    }
    
    return 0;
}
