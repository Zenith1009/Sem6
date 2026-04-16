%{
    int lines = 0, words = 0, chars = 0;
%}

%%
\n              { lines++; chars++; }
[^ \t\n]+       { words++; chars += yyleng; }
.               { chars++; }
%%

int yywrap() { return 1; }
int main(int argc, char *argv[]) {
    if (argc > 1) yyin = fopen(argv[1], "r");
    yylex();
    printf("Lines      : %d\n", lines);
    printf("Words      : %d\n", words);
    printf("Characters : %d\n", chars);
    return 0;
}
