%%
[0-9]*[02468]   { printf("%s is Even\n", yytext); }
[0-9]*[13579]   { printf("%s is Odd\n", yytext);  }
.|\\n           { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
