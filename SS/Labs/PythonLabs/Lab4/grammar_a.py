# Lab 4 — Grammar A: FIRST and FOLLOW sets
# Grammar A:
#   S -> aSbS | bSaS | epsilon

def main():
    print("\nGrammar A:")
    print("S -> aSbS | bSaS | ε\n")

    first_S = {'a', 'b', 'ε'}
    follow_S = {'$', 'a', 'b'}

    print("FIRST(S) = {", ", ".join(sorted(first_S)), "}")
    print()
    print("FOLLOW(S) = {", ", ".join(sorted(follow_S)), "}")
    print()

if __name__ == "__main__":
    main()
