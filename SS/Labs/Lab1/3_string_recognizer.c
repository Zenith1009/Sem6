#include <stdio.h>
#include <string.h>

int recognizePattern1(char str[]) {
    int i = 0, bCount = 0;
    
    while(str[i] == 'b') {
        bCount++;
        i++;
    }
    
    if(bCount == 0)
        return 0;
    
    while(str[i] == 'a')
        i++;
    
    return (str[i] == '\0');
}

int recognizePattern2(char str[]) {
    int i = 0, bCount = 0;
    
    while(str[i] == 'a')
        i++;
    
    while(str[i] == 'b') {
        bCount++;
        i++;
    }
    
    if(bCount == 0)
        return 0;
    
    while(str[i] == 'a')
        i++;
    
    return (str[i] == '\0');
}

int main() {
    char str[100];
    
    printf("Enter a string: ");
    scanf("%s", str);
    
    printf("\nPattern Recognition Results:\n");
    printf("-----------------------------\n");
    
    if(recognizePattern1(str))
        printf("Pattern 'b+a*': ACCEPTED\n");
    else
        printf("Pattern 'b+a*': REJECTED\n");
    
    if(recognizePattern2(str))
        printf("Pattern 'a*b+a*': ACCEPTED\n");
    else
        printf("Pattern 'a*b+a*': REJECTED\n");
    
    return 0;
}
