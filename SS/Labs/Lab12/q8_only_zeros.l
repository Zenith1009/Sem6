%%
0+      { printf("Accepted: \"%s\" (only zeros)\n", yytext); }
[^ \t\n]+   { printf("Rejected: \"%s\"\n", yytext); }
.|\\n   { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
