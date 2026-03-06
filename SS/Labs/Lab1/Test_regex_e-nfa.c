#include <stdio.h>
#include <string.h>

#define MAX 50

typedef struct {
    int state;
    char input[10];
    int next_state;
} Transition;

Transition dfa[MAX];
int trans_count = 0;
int state_count = 0;

void add_transition(int from, char symbol, int to) {
    dfa[trans_count].state = from;
    dfa[trans_count].input[0] = symbol;
    dfa[trans_count].input[1] = '\0';
    dfa[trans_count].next_state = to;
    trans_count++;
}

void build_dfa(char *regex) {
    state_count = 0;
    int i = 0;
    
    while(regex[i] != '\0') {
        char ch = regex[i];
        
        if(ch == '*') {
            add_transition(state_count, regex[i-1], state_count);
            state_count++;
        } 
        else if(ch == '+') {
            add_transition(state_count, regex[i-1], state_count + 1);
            add_transition(state_count + 1, regex[i-1], state_count + 1);
            state_count += 2;
        }
        else if(ch != '|' && (i == 0 || regex[i-1] != '*' && regex[i-1] != '+')) {
            add_transition(state_count, ch, state_count + 1);
            state_count++;
        }
        i++;
    }
}

void print_dfa() {
    printf("\n=== DFA Transition Table ===\n");
    printf("%-10s %-10s %-10s\n", "State", "Input", "Next State");
    printf("------------------------------------\n");
    
    for(int i = 0; i < trans_count; i++) {
        printf("q%-9d %-10s q%-9d\n", 
               dfa[i].state, 
               dfa[i].input, 
               dfa[i].next_state);
    }
    
    printf("------------------------------------\n");
    printf("Start State: q0\n");
    printf("Final State: q%d\n", state_count);
}

int validate_string(char *str) {
    int current_state = 0;
    int i = 0;
    
    while(str[i] != '\0') {
        int found = 0;
        
        for(int j = 0; j < trans_count; j++) {
            if(dfa[j].state == current_state && dfa[j].input[0] == str[i]) {
                current_state = dfa[j].next_state;
                found = 1;
                break;
            }
        }
        
        if(!found) {
            return 0;
        }
        i++;
    }
    
    return (current_state == state_count);
}

int main() {
    char regex[50], test_string[50];
    char choice;
    
    printf("Enter a regular expression (e.g., ab*, a+b, abc): ");
    scanf("%s", regex);
    
    build_dfa(regex);
    print_dfa();
    
    do {
        printf("\nTest a string? (y/n): ");
        scanf(" %c", &choice);
        
        if(choice == 'y' || choice == 'Y') {
            printf("Enter string to validate: ");
            scanf("%s", test_string);
            
            if(validate_string(test_string)) {
                printf("String ACCEPTED by DFA\n");
            } else {
                printf("String REJECTED by DFA\n");
            }
        }
    } while(choice == 'y' || choice == 'Y');
    
    return 0;
}
