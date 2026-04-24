# Viva Prep — Lab 10 & Lab 11

---
## LAB 10 — CLR(1) and LALR(1)
---

### Q: What is a parser? What type did you implement?
A parser checks if a token stream follows grammar rules. I implemented **bottom-up LR parsers** — they read left-to-right, build a rightmost derivation in reverse, using a **stack + parse table**.

---

### Q: What does CLR(1) stand for? How is it better than SLR(1)?
**Canonical LR(1).** The 1 = one lookahead symbol.
- **SLR(1)** reduces on any terminal in `FOLLOW(A)` — too broad, causes conflicts.
- **CLR(1)** attaches lookahead directly to each item: `[A → α•β, a]`. Reduce fires *only* on that exact `a`. More precise = more powerful.

---

### Q: What is an LR(1) item?
A production with a **dot** (how far parsed) + a **lookahead**:
```
[S → (•S), )]  →  seen '(', expecting S, reduce only if next token is ')'
```
Dot moves right on each shift.

---

### Q: What is closure?
Given `[A → α•Bβ, a]`, add all B-productions with lookahead = `FIRST(βa)`.
Repeat until no new items. It represents *everything we could be parsing* from this state.

---

### Q: What is goto?
`goto(I, X)` = advance dot past X in every item of state I, then take closure.
Builds transitions between states — forms the LR automaton.

---

### Q: How is the Action/Goto table filled?
For each state:
- `[A → α•aβ, _]`, `a` is terminal → **Shift** to `goto(I, a)`
- `[A → α•, a]` dot at end → **Reduce** by this production on lookahead `a`
- `[S' → S•, $]` → **Accept**
- Non-terminal X in goto → fill **Goto table**

---

### Q: Did your CLR(1) grammar have conflicts?
No. `S → (S) | a` produces **10 states, zero conflicts**. The grammar is CLR(1).

---

### Q: What is LALR(1)? How does it differ from CLR(1)?

| | CLR(1) | LALR(1) |
|---|---|---|
| States | More (no merge) | Fewer (**merge by core**) |
| Power | Stronger | Slightly weaker |
| Conflicts possible | No | Reduce-Reduce on merge |
| Real use | Theory | **yacc, bison** |

Algorithm: build CLR(1), then merge states with the same **LR(0) core** (same items, ignore lookaheads), union the lookaheads.

---

### Q: Which states were merged for `S→AA, A→aA|b`?

| LR(1) pair | Core | Merged lookahead |
|---|---|---|
| I3 + I6 | `A→a•A, A→•aA, A→•b` | {a,b} ∪ {\$} = {a,b,\$} |
| I4 + I7 | `A→b•` | {a,b} ∪ {\$} = {a,b,\$} |
| I8 + I9 | `A→aA•` | {a,b} ∪ {\$} = {a,b,\$} |

Result: **7 LALR(1) states**, no conflicts.

---

### Q: Walk through parsing `aaabb`.
```
Stack           Input    Action
[0]             aaabb$   Shift
[0,3]           aabb$    Shift
[0,3,3]         abb$     Shift
[0,3,3,3]       bb$      Shift
[0,3,3,3,2]     b$       Reduce A→b
[0,3,3,3,6]     b$       Reduce A→aA
[0,3,3,6]       b$       Reduce A→aA
[0,3,6]         b$       Reduce A→aA   ← first A = "aaab"
[0,1]           b$       Shift
[0,1,2]         $        Reduce A→b    ← second A = "b"
[0,1,5]         $        Reduce S→AA
[0,4]           $        ACCEPT
```

---

### Q: Why LALR over CLR in real compilers?
Fewer states = less memory and faster parsing, with nearly the same power. **GNU bison and yacc are LALR(1)** parsers. CLR is mainly academic.

---
## LAB 11 — Lex Programs
---

### Q: What is Lex?
A **lexical analyzer generator**. You write pattern-action rules; Lex generates a C scanner using a DFA. The main function is `yylex()`.

---

### Q: What are the three sections of a Lex file?
```
%{ C declarations %}
%%
pattern   { action }    ← core rules
%%
main() and helpers
```

---

### Q: What is `yywrap()`? Why return 1?
Called at end-of-file. **Return 1** = stop. Return 0 = continue (multiple files). We always return 1 (single input).

---

### Q: What is `yytext` and `yyleng`?
- `yytext` → pointer to the **matched string**
- `yyleng` → **length** of the match

In Q1: `chars += yyleng` counts all characters in a word-token at once.

---

### Q: How does Lex choose between multiple matching rules?
1. **Longest match wins** always
2. On a tie → **first rule in file wins**

That's why in Q4, the fraction pattern comes before the integer pattern.

---

### Q: Q1 — How do you count lines, words, characters?
```lex
\n          { lines++; chars++; }
[^ \t\n]+   { words++; chars += yyleng; }
.           { chars++; }
```

---

### Q: Q3 — How does lowercase→uppercase work without `toupper()`?
```lex
[a-z]  { printf("%c", yytext[0] - 32); }
```
ASCII gap between `'a'`(97) and `'A'`(65) is exactly **32**. Subtract 32 = uppercase.

---

### Q: Q4 — Why is the fraction rule before the integer rule?
`-1.5` could partially match `-[0-9]+` (as `-1`). Longest match would still pick the fraction, but placing fractions first makes intent explicit — a good Lex practice.

---

### Q: Q5 — Explain the mobile regex.
```
\+91[6-9][0-9]{9}
```
- `\+91` → literal `+91` (`+` escaped)
- `[6-9]` → valid Indian mobile start (6,7,8,9)
- `[0-9]{9}` → exactly 9 more digits = 10-digit number total

---

### Q: Q7 — How do you detect compound sentences?
```lex
[Ff]or|[Aa]nd|[Nn]or|[Bb]ut|[Oo]r|[Yy]et|[Ss]o  { compound = 1; }
```
FANBOYS conjunctions join two independent clauses. If any found → "Compound", else → "Simple".

---

### Q: Q6 — How does the calculator work in one rule?
The entire expression like `3.5 + 2` is matched as one token, then:
```c
sscanf(yytext, "%f %c %f", &a, &op, &b);
```
splits out the two operands and operator. A switch on `op` computes the result.

---

### Q: How do you compile and run a Lex file?
```bash
flex file.l              # generates lex.yy.c
gcc lex.yy.c -o out -ll  # -ll = lex library (macOS: -ll, Linux: -lfl)
./out < input.txt
```

---

### Q: One-line difference between SLR / LALR / CLR?
- **SLR(1)** — uses FOLLOW sets, weakest, fewest states
- **LALR(1)** — merges CLR states by LR(0) core, used in real tools (yacc/bison)
- **CLR(1)** — full LR(1) items, strongest, most states, mainly theoretical
