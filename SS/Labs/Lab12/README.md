# System Software Lab 12: Lex Programs

## Compile & Run (any question)
```bash
flex <file>.l
gcc lex.yy.c -o <output> -ll    # macOS
# or: gcc lex.yy.c -o <output> -lfl  # Linux
```

> For Q4 (Armstrong), link math: `gcc lex.yy.c -o q4 -ll -lm`

---

## Q1 — Length of a String
```bash
flex q1_length.l && gcc lex.yy.c -o q1 -ll
echo "hello world" | ./q1
```
```
String: "hello", Length: 5
String: "world", Length: 5
```

## Q2 — Accept String Starting with Vowel
```bash
flex q2_vowel_start.l && gcc lex.yy.c -o q2 -ll
printf "apple\nbanana\norange\ncat\n" | ./q2
```
```
Accepted: apple
Rejected: banana
Accepted: orange
Rejected: cat
```

## Q3 — Even or Odd Number
```bash
flex q3_even_odd.l && gcc lex.yy.c -o q3 -ll
echo "3 18 7 100 -1" | ./q3
```
```
3 is Odd
18 is Even
7 is Odd
100 is Even
```
> Matches last digit: if it's in `[02468]` → Even, else Odd.

## Q4 — Armstrong Number
```bash
flex q4_armstrong.l && gcc lex.yy.c -o q4 -ll -lm
echo "153 370 371 407 100 9" | ./q4
```
```
153 is an Armstrong number
370 is an Armstrong number
371 is an Armstrong number
407 is an Armstrong number
100 is NOT an Armstrong number
9 is an Armstrong number
```
> Sum of each digit raised to the power of number of digits equals the number itself.

## Q5 — Check Whether Input is a Digit
```bash
flex q5_digit_check.l && gcc lex.yy.c -o q5 -ll
printf "5\nabc\n3\nhello\n" | ./q5
```
```
'5' is a digit
'abc' is NOT a digit
'3' is a digit
'hello' is NOT a digit
```

## Q6 — Perfect Numbers
```bash
flex q6_perfect.l && gcc lex.yy.c -o q6 -ll
echo "6 28 496 12 100" | ./q6
```
```
6 is a Perfect number
28 is a Perfect number
496 is a Perfect number
12 is NOT a Perfect number
100 is NOT a Perfect number
```
> A perfect number equals the sum of its proper divisors (e.g. 6 = 1+2+3).

## Q7 — Even Number of 'a's over {a, b}
```bash
flex q7_even_a.l && gcc lex.yy.c -o q7 -ll
printf "bb\naba\naabb\nabba\na\n" | ./q7
```
```
Accepted: "bb" (even number of 'a's)
Rejected: "aba" (odd number of 'a's)
Accepted: "aabb" (even number of 'a's)
Accepted: "abba" (even number of 'a's)
Rejected: "a" (odd number of 'a's)
```
> Simulates a 2-state DFA; XORs state for each 'a' seen. Zero 'a's = even = accepted.

## Q8 — Accept String with 0 Only
```bash
flex q8_only_zeros.l && gcc lex.yy.c -o q8 -ll
printf "000\n0\n010\nabc\n0000\n" | ./q8
```
```
Accepted: "000" (only zeros)
Accepted: "0" (only zeros)
Rejected: "010"
Rejected: "abc"
Accepted: "0000" (only zeros)
```
