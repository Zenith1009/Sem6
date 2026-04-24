# Lab 5 — LL(1) Parser
# Grammar:
#   E  -> T A      (A = E')
#   A  -> + T A | epsilon
#   T  -> F B      (B = T')
#   B  -> * F B | epsilon
#   F  -> id | ( E )
# Terminals: id(i), +, *, (, ), $

NT = ['E', 'A', 'T', 'B', 'F']   # A = E', B = T'
TM = ['i', '+', '*', '(', ')', '$']   # i = id

prods = [
    ('E', 'TA'), ('A', '+TA'), ('A', 'e'), ('T', 'FB'),
    ('B', '*FB'), ('B', 'e'), ('F', 'i'),  ('F', '(E)')
]

# ── Helpers ──────────────────────────────────────────────────────────────

def nt_idx(c):
    return NT.index(c) if c in NT else -1

def t_idx(c):
    return TM.index(c) if c in TM else -1

def is_terminal(c):
    return t_idx(c) != -1

# ── FIRST of a string ────────────────────────────────────────────────────

def first_of_str(s, first_sets):
    out = set()
    if not s or s == 'e':
        return {'e'}
    for sym in s:
        if is_terminal(sym):
            out.add(sym)
            return out
        ni = nt_idx(sym)
        if ni == -1:
            return out
        out |= first_sets[ni] - {'e'}
        if 'e' not in first_sets[ni]:
            return out
    out.add('e')
    return out

# ── Compute FIRST ────────────────────────────────────────────────────────

def compute_first():
    first = [set() for _ in NT]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in prods:
            a = nt_idx(lhs)
            f = first_of_str(rhs, first)
            before = len(first[a])
            first[a] |= f
            if len(first[a]) != before:
                changed = True
    return first

# ── Compute FOLLOW ───────────────────────────────────────────────────────

def compute_follow(first):
    follow = [set() for _ in NT]
    follow[nt_idx('E')].add('$')
    changed = True
    while changed:
        changed = False
        for lhs, rhs in prods:
            a = nt_idx(lhs)
            for j, sym in enumerate(rhs):
                b = nt_idx(sym)
                if b == -1:
                    continue
                fs = first_of_str(rhs[j+1:], first) if j + 1 < len(rhs) else {'e'}
                before = len(follow[b])
                follow[b] |= fs - {'e'}
                if 'e' in fs:
                    follow[b] |= follow[a]
                if len(follow[b]) != before:
                    changed = True
    return follow

# ── Build LL(1) Table ────────────────────────────────────────────────────

def build_table(first, follow):
    table = [['-'] * len(TM) for _ in NT]
    for i, (lhs, rhs) in enumerate(prods):
        a = nt_idx(lhs)
        f = first_of_str(rhs, first)
        for sym in f:
            if sym == 'e':
                continue
            c = t_idx(sym)
            if c != -1:
                table[a][c] = rhs
        if 'e' in f:
            for sym in follow[a]:
                c = t_idx(sym)
                if c != -1:
                    table[a][c] = 'e'
    return table

# ── Normalize input ──────────────────────────────────────────────────────

def normalize(raw):
    out = []
    i = 0
    raw = raw.strip()
    while i < len(raw):
        if raw[i:i+2] == 'id':
            out.append('i')
            i += 2
        elif raw[i] in '+*()':
            out.append(raw[i])
            i += 1
        elif raw[i] == ' ':
            i += 1
        else:
            return None  # invalid token
    out.append('$')
    return out

# ── Parse ────────────────────────────────────────────────────────────────

def parse(table, inp):
    stack = ['$', 'E']
    ip = 0
    while stack:
        X = stack[-1]
        a = inp[ip]
        if X == '$' and a == '$':
            return True
        if is_terminal(X):
            if X != a:
                return False
            stack.pop()
            ip += 1
        else:
            r = nt_idx(X)
            c = t_idx(a)
            if r == -1 or c == -1 or table[r][c] == '-':
                return False
            stack.pop()
            rhs = table[r][c]
            if rhs != 'e':
                for ch in reversed(rhs):
                    stack.append(ch)
    return False

# ── Print Table ──────────────────────────────────────────────────────────

def print_table(table):
    print("\nLL(1) Parse Table (A=E', B=T'):\n")
    header = "      " + "".join(f"{t:<8}" for t in TM)
    print(header)
    for i, row in enumerate(table):
        print(f"{NT[i]:<4}  " + "".join(f"{cell:<8}" for cell in row))

# ── Main ─────────────────────────────────────────────────────────────────

def main():
    first  = compute_first()
    follow = compute_follow(first)
    table  = build_table(first, follow)
    print_table(table)

    raw = input("\nEnter input string (use id, +, *, (, )): ").strip()
    inp = normalize(raw)
    if inp is None:
        print("Invalid token in input!")
    else:
        print("Accepted" if parse(table, inp) else "Rejected")

if __name__ == "__main__":
    main()
