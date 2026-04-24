
# Lab 1 — Lexical Analyzer for a C statement

KEYWORDS = {"int", "float", "if", "else", "while", "for",
            "return", "void", "char", "main", "printf", "scanf"}

TWO_CHAR_OPS = {">=", "<=", "==", "!="}
ONE_CHAR_OPS = set("+-*/=<>")
SPECIAL_SYMS = set(";,(){}")

def tokenize(inp):
    tokens = []
    i = 0
    while i < len(inp):
        ch = inp[i]

        if ch in ' \t\n':
            i += 1
            continue

        # String literal
        if ch == '"':
            i += 1
            j = i
            while i < len(inp) and inp[i] != '"':
                i += 1
            tokens.append(("String Literal", inp[j:i]))
            if i < len(inp):
                i += 1  # skip closing quote
            continue

        # Identifier or keyword
        if ch.isalpha() or ch == '_':
            j = i
            while i < len(inp) and (inp[i].isalnum() or inp[i] == '_'):
                i += 1
            word = inp[j:i]
            label = "Keyword" if word in KEYWORDS else "Identifier"
            tokens.append((label, word))
            continue

        # Number
        if ch.isdigit():
            j = i
            while i < len(inp) and inp[i].isdigit():
                i += 1
            tokens.append(("Number", inp[j:i]))
            continue

        # Two-char operators
        two = inp[i:i+2]
        if two in TWO_CHAR_OPS:
            tokens.append(("Operator", two))
            i += 2
            continue

        # One-char operators
        if ch in ONE_CHAR_OPS:
            tokens.append(("Operator", ch))
            i += 1
            continue

        # Special symbols
        if ch in SPECIAL_SYMS:
            tokens.append(("Special Symbol", ch))
            i += 1
            continue

        i += 1  # skip unknown

    return tokens

def main():
    inp = input("Enter a C statement: ")
    tokens = tokenize(inp)
    print("\nTokens identified:")
    print("-------------------")
    for label, val in tokens:
        print(f"{label}: {val}")

if __name__ == "__main__":
    main()
