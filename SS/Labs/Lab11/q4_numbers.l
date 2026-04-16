%{
    int pos_int = 0, neg_int = 0, pos_frac = 0, neg_frac = 0;
%}

%%
-[0-9]+"."[0-9]+        { neg_frac++; }
[+]?[0-9]+"."[0-9]+     { pos_frac++; }
-[0-9]+                 { neg_int++;  }
[+]?[0-9]+              { pos_int++;  }
.|\n                    { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    printf("Positive integers  : %d\n", pos_int);
    printf("Negative integers  : %d\n", neg_int);
    printf("Positive fractions : %d\n", pos_frac);
    printf("Negative fractions : %d\n", neg_frac);
    return 0;
}
