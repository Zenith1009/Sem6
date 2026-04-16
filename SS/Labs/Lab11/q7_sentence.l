%{
    int compound = 0;
%}

%%
[Ff]or|[Aa]nd|[Nn]or|[Bb]ut|[Oo]r|[Yy]et|[Ss]o   { compound = 1; }
.|\n                                                { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    printf("%s sentence\n", compound ? "Compound" : "Simple");
    return 0;
}
