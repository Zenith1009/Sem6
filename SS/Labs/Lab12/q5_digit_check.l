%%
[0-9]       { printf("'%s' is a digit\n", yytext); }
[^ \t\n]+   { printf("'%s' is NOT a digit\n", yytext); }
.|\\n       { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
