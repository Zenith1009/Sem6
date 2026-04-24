%{
    int is_perfect(int n) {
        if (n < 2) return 0;
        int sum = 1, i;
        for (i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                sum += i;
                if (i != n / i) sum += n / i;
            }
        }
        return sum == n;
    }
%}

%%
[0-9]+  {
            int n = atoi(yytext);
            if (is_perfect(n))
                printf("%d is a Perfect number\n", n);
            else
                printf("%d is NOT a Perfect number\n", n);
        }
.|\\n   { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
