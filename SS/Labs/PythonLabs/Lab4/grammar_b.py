# Lab 4 — Grammar B: FIRST and FOLLOW sets
# Grammar B:
#   E  -> T E'
#   E' -> +T E' | epsilon
#   T  -> F T'
#   T' -> *F T' | epsilon
#   F  -> (E) | id

def compute_first():
    return {
        'E':       {'(', 'id'},
        "E'":      {'+', 'ε'},
        'T':       {'(', 'id'},
        "T'":      {'*', 'ε'},
        'F':       {'(', 'id'},
    }

def compute_follow():
    return {
        'E':       {'$', ')'},
        "E'":      {'$', ')'},
        'T':       {'+', '$', ')'},
        "T'":      {'+', '$', ')'},
        'F':       {'*', '+', '$', ')'},
    }

def print_sets(label, sets):
    print(f"\n{label}:")
    for nt, s in sets.items():
        members = ", ".join(sorted(s))
        print(f"  {label.split()[0]}({nt}) = {{ {members} }}")

def main():
    print("\nGrammar B:")
    print("E  -> T E'")
    print("E' -> +T E' | ε")
    print("T  -> F T'")
    print("T' -> *F T' | ε")
    print("F  -> (E) | id")

    first  = compute_first()
    follow = compute_follow()

    print_sets("FIRST SETS", first)
    print_sets("FOLLOW SETS", follow)
    print()

if __name__ == "__main__":
    main()
