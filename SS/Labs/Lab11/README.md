# System Software Lab 11: Lex Programs

## Compile & Run (any question)
```bash
flex <file>.l
gcc lex.yy.c -o <output> -ll    # macOS
# or: gcc lex.yy.c -o <output> -lfl  # Linux
```

---

## Q1 — Count Lines, Words, Characters
```bash
flex q1_count.l && gcc lex.yy.c -o q1 -ll
./q1 sample.txt
```
```
Lines      : 2
Words      : 14
Characters : 80
```

## Q2 — Count Vowels and Consonants
```bash
flex q2_vowels.l && gcc lex.yy.c -o q2 -ll
echo "Hello World" | ./q2
```
```
Vowels     : 3
Consonants : 7
```

## Q3 — Lowercase to Uppercase
```bash
flex q3_uppercase.l && gcc lex.yy.c -o q3 -ll
echo "abc DEF" | ./q3
```
```
ABC DEF
```

## Q4 — Count +ve / –ve Integers and Fractions
```bash
flex q4_numbers.l && gcc lex.yy.c -o q4 -ll
echo "3 -2 1.5 -0.75 100 -50" | ./q4
```
```
Positive integers  : 2
Negative integers  : 2
Positive fractions : 1
Negative fractions : 1
```
> Fractions are matched before integers (longer match wins in Lex).

## Q5 — Validate Mobile Number and Email
```bash
flex q5_validate.l && gcc lex.yy.c -o q5 -ll
printf "+919876543210\nnaish@example.com\n123abc\n" | ./q5
```
```
Mobile : Valid
Email  : Valid
Invalid: 123abc
```
- Mobile pattern: `+91` followed by 10 digits starting with 6–9
- Each line of input is matched independently

## Q6 — Simple Calculator
```bash
flex q6_calculator.l && gcc lex.yy.c -o q6 -ll
printf "3.5 + 2\n10 / 4\n" | ./q6
```
```
Result: 5.5
Result: 2.5
```

## Q7 — Simple or Compound Sentence
```bash
flex q7_sentence.l && gcc lex.yy.c -o q7 -ll
echo "I went to the market and bought apples." | ./q7
echo "She sings beautifully." | ./q7
```
```
Compound sentence
Simple sentence
```
> Uses FANBOYS conjunctions: `for, and, nor, but, or, yet, so`
