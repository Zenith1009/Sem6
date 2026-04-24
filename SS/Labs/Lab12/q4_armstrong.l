%{
    #include <math.h>
    #include <string.h>

    int is_armstrong(int n) {
        int temp = n, digits = 0, sum = 0;
        while (temp) { digits++; temp /= 10; }
        temp = n;
        while (temp) {
            int d = temp % 10;
            sum += (int)round(pow(d, digits));
            temp /= 10;
        }
        return sum == n;
    }
%}

%%
[0-9]+  {
            int n = atoi(yytext);
            if (is_armstrong(n))
                printf("%d is an Armstrong number\n", n);
            else
                printf("%d is NOT an Armstrong number\n", n);
        }
.|\\n   { }
%%

int yywrap() { return 1; }
int main() {
    yylex();
    return 0;
}
