%{
    int len = 0;
%}

%%
[^ \t\n]+   { len += yyleng; printf("String: \"%s\", Length: %d\n", yytext, len); len = 0; }
.|\\n       { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
