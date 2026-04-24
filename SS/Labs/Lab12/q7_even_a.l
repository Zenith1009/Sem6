%{
    /* Accepts strings over {a, b} with even number of 'a's  */
    /* Uses manual DFA state: state 0 = even 'a's (accept), state 1 = odd 'a's */
    int state = 0;
%}

%%
[ab]+   {
            int i;
            state = 0;
            for (i = 0; i < yyleng; i++) {
                if (yytext[i] == 'a') state ^= 1;
            }
            if (state == 0)
                printf("Accepted: \"%s\" (even number of 'a's)\n", yytext);
            else
                printf("Rejected: \"%s\" (odd number of 'a's)\n", yytext);
        }
[^ \t\n]+   { printf("Rejected: \"%s\" (invalid characters)\n", yytext); }
.|\\n       { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
