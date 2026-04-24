# Lab 2 — Arithmetic Expression Analyzer
# Identifies identifiers and operators in a valid arithmetic expression

def analyze(expr):
    identifiers = []
    operators = []
    valid = True
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch in ' \t\n':
            i += 1
            continue

        if ch in '+-*/%':
            operators.append(ch)
            i += 1

        elif ch.isalpha():
            j = i
            while i < len(expr) and expr[i].isalnum():
                i += 1
            identifiers.append(expr[j:i])

        elif ch.isdigit():
            while i < len(expr) and expr[i].isdigit():
                i += 1

        elif ch in '()':
            i += 1

        else:
            valid = False
            break

    return valid, identifiers, operators

def main():
    expr = input("Enter arithmetic expression: ")
    valid, identifiers, operators = analyze(expr)

    if valid:
        print("\nVALID arithmetic expression")
        print("Identifiers:", " ".join(identifiers))
        print("Operators:  ", " ".join(operators))
    else:
        print("\nINVALID expression")

if __name__ == "__main__":
    main()
