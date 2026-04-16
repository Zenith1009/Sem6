%{
    #include <stdlib.h>
    float a, b;
    char op;
%}

%%
[+-]?[0-9]+("."[0-9]+)?[ \t]*[+\-*/][ \t]*[+-]?[0-9]+("."[0-9]+)? {
    sscanf(yytext, "%f %c %f", &a, &op, &b);
    switch (op) {
        case '+': printf("Result: %g\n", a + b); break;
        case '-': printf("Result: %g\n", a - b); break;
        case '*': printf("Result: %g\n", a * b); break;
        case '/': if (b != 0) printf("Result: %g\n", a / b);
                  else        printf("Division by zero\n"); break;
    }
}
.|\n    { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
