# Lab 8 — LL(1) Parser with FIRST/FOLLOW computation
# Grammar:
#   S -> aBDh
#   B -> cC
#   C -> bC | #   (# = epsilon)
#   D -> EF
#   E -> g | #
#   F -> f | #

PRODS = [
    ('S', 'aBDh'),
    ('B', 'cC'),
    ('C', 'bC'),
    ('C', '#'),
    ('D', 'EF'),
    ('E', 'g'),
    ('E', '#'),
    ('F', 'f'),
    ('F', '#'),
]

NONTERMS = ['S', 'B', 'C', 'D', 'E', 'F']

def nt_index(c):
    return NONTERMS.index(c) if c in NONTERMS else -1

def is_upper(c):
    return c.isupper()

# ── FIRST of a string ────────────────────────────────────────────────────

def first_of_str(s, first_sets):
    out = set()
    if not s or s == '#':
        return {'#'}
    all_eps = True
    for sym in s:
        if not is_upper(sym):
            out.add(sym)
            all_eps = False
            break
        idx = nt_index(sym)
        if idx == -1:
            all_eps = False
            break
        out |= first_sets[idx] - {'#'}
        if '#' not in first_sets[idx]:
            all_eps = False
            break
    if all_eps:
        out.add('#')
    return out

# ── Compute FIRST sets ───────────────────────────────────────────────────

def compute_first():
    first = [set() for _ in NONTERMS]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in PRODS:
            i = nt_index(lhs)
            f = first_of_str(rhs, first)
            before = len(first[i])
            first[i] |= f
            if len(first[i]) != before:
                changed = True
    return first

# ── Compute FOLLOW sets ──────────────────────────────────────────────────

def compute_follow(first):
    follow = [set() for _ in NONTERMS]
    follow[nt_index('S')].add('$')
    changed = True
    while changed:
        changed = False
        for lhs, rhs in PRODS:
            li = nt_index(lhs)
            for j, sym in enumerate(rhs):
                if not is_upper(sym):
                    continue
                bi = nt_index(sym)
                if bi == -1:
                    continue
                beta = rhs[j+1:]
                fb = first_of_str(beta, first) if beta else {'#'}
                before = len(follow[bi])
                follow[bi] |= fb - {'#'}
                if '#' in fb:
                    follow[bi] |= follow[li]
                if len(follow[bi]) != before:
                    changed = True
    return follow

# ── Collect terminals ────────────────────────────────────────────────────

def collect_terminals():
    terms = set()
    for _, rhs in PRODS:
        for c in rhs:
            if not is_upper(c) and c != '#':
                terms.add(c)
    terms.add('$')
    return sorted(terms)

# ── Build LL(1) Table ────────────────────────────────────────────────────

def build_table(first, follow):
    terms = collect_terminals()
    # table[nt][terminal] = production index or -1
    table = {nt: {t: -1 for t in terms} for nt in NONTERMS}
    is_ll1 = True

    for i, (lhs, rhs) in enumerate(PRODS):
        fa = first_of_str(rhs, first)
        for sym in fa:
            if sym == '#':
                continue
            if sym in table[lhs]:
                if table[lhs][sym] != -1 and table[lhs][sym] != i:
                    is_ll1 = False
                table[lhs][sym] = i
        if '#' in fa:
            for sym in follow[nt_index(lhs)]:
                if sym in table[lhs]:
                    if table[lhs][sym] != -1 and table[lhs][sym] != i:
                        is_ll1 = False
                    table[lhs][sym] = i

    return table, terms, is_ll1

# ── Print ────────────────────────────────────────────────────────────────

def print_first_follow(first, follow):
    print("\nFIRST Sets:")
    for i, nt in enumerate(NONTERMS):
        print(f"  FIRST({nt}) = {{ {', '.join(sorted(first[i]))} }}")
    print("\nFOLLOW Sets:")
    for i, nt in enumerate(NONTERMS):
        print(f"  FOLLOW({nt}) = {{ {', '.join(sorted(follow[i]))} }}")

def print_table(table, terms):
    print("\nLL(1) Parsing Table\n")
    header = f"{'NT/T':<6}" + "".join(f"{t:<12}" for t in terms)
    print(header)
    for nt in NONTERMS:
        row = f"{nt:<6}"
        for t in terms:
            p = table[nt][t]
            if p == -1:
                cell = '-'
            else:
                lhs, rhs = PRODS[p]
                cell = f"{lhs}->{rhs}"
            row += f"{cell:<12}"
        print(row)

# ── Main ─────────────────────────────────────────────────────────────────

def main():
    print("Given Grammar:")
    print("S -> aBDh")
    print("B -> cC")
    print("C -> bC | #")
    print("D -> EF")
    print("E -> g | #")
    print("F -> f | #")

    first  = compute_first()
    follow = compute_follow(first)
    table, terms, is_ll1 = build_table(first, follow)

    print_first_follow(first, follow)
    print_table(table, terms)

    status = "Grammar is LL(1)." if is_ll1 else "Grammar is NOT LL(1). (Conflict found)"
    print(f"\nGrammar status: {status}")

if __name__ == "__main__":
    main()
