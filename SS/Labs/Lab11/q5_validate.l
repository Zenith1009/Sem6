%%
\+91[6-9][0-9]{9}                                   { printf("Mobile : Valid\n"); }
[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}  { printf("Email  : Valid\n"); }
[^\n]+                                              { printf("Invalid: %s\n", yytext); }
\n                                                  { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
