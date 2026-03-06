// Program to identify whether a given line is a comment or not
#include <stdio.h>
#include <string.h>

int main() {
    char line[100];
    int i = 0;
    
    printf("Enter a line: ");
    fgets(line, sizeof(line), stdin);
    
    // Skip leading spaces
    while (line[i] == ' ' || line[i] == '\t')
        i++;
    
    printf("Result: ");
    
    // Check for single-line comment //
    if (line[i] == '/' && line[i+1] == '/') {
        printf("Single-line comment\n");
    }
    // Check for multi-line comment start /*
    else if (line[i] == '/' && line[i+1] == '*') {
        // Check if it ends on same line
        if (strstr(line, "*/") != NULL)
            printf("Multi-line comment (complete)\n");
        else
            printf("Multi-line comment START\n");
    }
    // Check for multi-line comment end */
    else if (strstr(line, "*/") != NULL) {
        printf("Multi-line comment END\n");
    }
    else {
        printf("NOT a comment\n");
    }
    
    return 0;
}
