%%
[aeiouAEIOU][a-zA-Z]*   { printf("Accepted: %s\n", yytext); }
[a-zA-Z]+               { printf("Rejected: %s\n", yytext); }
.|\\n                   { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
