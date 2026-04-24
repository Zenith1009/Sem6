# Lab 9 — SLR(1) Parser with automaton construction
# Grammar:
#   S' -> S
#   S  -> aBDh
#   B  -> cC
#   C  -> bC | epsilon
#   D  -> EF
#   E  -> g | epsilon
#   F  -> f | epsilon

# ── Productions ──────────────────────────────────────────────────────────
# Using '#' for epsilon

PRODS = [
    ("'", "S"),      # 0: S' -> S  (augmented)
    ('S', "aBDh"),   # 1
    ('B', "cC"),     # 2
    ('C', "bC"),     # 3
    ('C', "#"),      # 4
    ('D', "EF"),     # 5
    ('E', "g"),      # 6
    ('E', "#"),      # 7
    ('F', "f"),      # 8
    ('F', "#"),      # 9
]

NT_SYMS = ["'", 'S', 'B', 'C', 'D', 'E', 'F']
TM_SYMS = ['a', 'b', 'c', 'f', 'g', 'h', '$']

def ni(c): return NT_SYMS.index(c) if c in NT_SYMS else -1
def ti(c): return TM_SYMS.index(c)  if c in TM_SYMS else -1

# ── FIRST / FOLLOW ───────────────────────────────────────────────────────

def first_str(s, FIRST):
    out = set()
    if not s or s == '#':
        return {'#'}
    all_eps = True
    for sym in s:
        idx = ni(sym)
        if idx < 0:
            out.add(sym); all_eps = False; break
        out |= FIRST[idx] - {'#'}
        if '#' not in FIRST[idx]:
            all_eps = False; break
    if all_eps: out.add('#')
    return out

def compute_first():
    FIRST = [set() for _ in NT_SYMS]
    ch = True
    while ch:
        ch = False
        for lhs, rhs in PRODS:
            li = ni(lhs)
            f = first_str(rhs, FIRST)
            before = len(FIRST[li])
            FIRST[li] |= f
            if len(FIRST[li]) != before: ch = True
    return FIRST

def compute_follow(FIRST):
    FOLLOW = [set() for _ in NT_SYMS]
    FOLLOW[ni("'")].add('$')
    FOLLOW[ni('S')].add('$')
    ch = True
    while ch:
        ch = False
        for lhs, rhs in PRODS:
            li = ni(lhs)
            if rhs == '#': continue
            for j, sym in enumerate(rhs):
                bi = ni(sym)
                if bi < 0: continue
                fb = first_str(rhs[j+1:], FIRST) if j + 1 < len(rhs) else {'#'}
                before = len(FOLLOW[bi])
                FOLLOW[bi] |= fb - {'#'}
                if '#' in fb: FOLLOW[bi] |= FOLLOW[li]
                if len(FOLLOW[bi]) != before: ch = True
    return FOLLOW

# ── LR(0) Item / State / Automaton ───────────────────────────────────────

def closure(items):
    S = set(items)
    ch = True
    while ch:
        ch = False
        for (p, dot) in list(S):
            rhs = PRODS[p][1]
            if rhs == '#' or dot >= len(rhs): continue
            X = rhs[dot]
            if ni(X) < 0: continue
            for i, (l, _) in enumerate(PRODS):
                if l == X and (i, 0) not in S:
                    S.add((i, 0)); ch = True
    return frozenset(S)

def goto_set(items, X):
    moved = {(p, dot+1) for (p, dot) in items
             if PRODS[p][1] != '#' and dot < len(PRODS[p][1]) and PRODS[p][1][dot] == X}
    return closure(moved) if moved else frozenset()

def build_automaton():
    s0 = closure({(0, 0)})
    states = [s0]
    idx    = {s0: 0}
    trans  = {}
    i = 0
    all_syms = NT_SYMS + TM_SYMS
    while i < len(states):
        for X in all_syms:
            nxt = goto_set(states[i], X)
            if not nxt: continue
            if nxt not in idx:
                idx[nxt] = len(states)
                states.append(nxt)
            trans[(i, X)] = idx[nxt]
        i += 1
    return states, trans

# ── Build SLR(1) Tables ───────────────────────────────────────────────────

ACC = 'acc'

def build_slr(states, trans, FIRST, FOLLOW):
    # action[state][term_idx] = 'sX' | 'rY' | 'acc' | None
    action = [[None] * len(TM_SYMS) for _ in states]
    go_nt  = [[-1]   * len(NT_SYMS) for _ in states]
    conflict = False

    def set_act(s, t, v):
        nonlocal conflict
        if action[s][t] is not None and action[s][t] != v:
            print(f"CONFLICT state {s} term {TM_SYMS[t]}")
            conflict = True
        action[s][t] = v

    for i, st in enumerate(states):
        # Shifts from transitions
        for j, tm in enumerate(TM_SYMS):
            if (i, tm) in trans:
                set_act(i, j, f's{trans[(i, tm)]}')
        # Reduce / accept from complete items
        for (p, dot) in st:
            lhs, rhs = PRODS[p]
            if rhs != '#' and dot < len(rhs): continue
            if p == 0:
                set_act(i, ti('$'), ACC)
            else:
                li = ni(lhs)
                for j, tm in enumerate(TM_SYMS):
                    if tm in FOLLOW[li]:
                        set_act(i, j, f'r{p}')
        # GOTO for non-terminals
        for j, nt in enumerate(NT_SYMS):
            if (i, nt) in trans:
                go_nt[i][j] = trans[(i, nt)]

    return action, go_nt, conflict

# ── Print ─────────────────────────────────────────────────────────────────

def print_sets(FIRST, FOLLOW):
    print("\nFIRST Sets:")
    for i in range(1, len(NT_SYMS)):   # skip S'
        s = ', '.join(('ε' if c=='#' else c) for c in sorted(FIRST[i]))
        print(f"  FIRST({NT_SYMS[i]}) = {{ {s} }}")
    print("\nFOLLOW Sets:")
    for i in range(1, len(NT_SYMS)):
        s = ', '.join(sorted(FOLLOW[i]))
        print(f"  FOLLOW({NT_SYMS[i]}) = {{ {s} }}")

def print_table(action, go_nt, n_states):
    print("\nSLR(1) Parsing Table:")
    hdr = f"{'St':>3} | " + "  ".join(f"{t:<4}" for t in TM_SYMS) + " | " + "  ".join(f"{nt:<4}" for nt in NT_SYMS[1:])
    print(hdr)
    print("-" * len(hdr))
    for i in range(n_states):
        acts = "  ".join(f"{(action[i][j] or '-'):<4}" for j in range(len(TM_SYMS)))
        gos  = "  ".join(f"{(str(go_nt[i][j]) if go_nt[i][j]>=0 else '-'):<4}" for j in range(1, len(NT_SYMS)))
        print(f"{i:>3} | {acts} | {gos}")

# ── Parse ─────────────────────────────────────────────────────────────────

def parse(action, go_nt, inp_str):
    buf   = list(inp_str) + ['$']
    stack = [0]
    ip    = 0

    print(f"\n{'Stack':<22} {'Input':<14} Action")
    print("-" * 52)

    while True:
        state = stack[-1]
        t     = buf[ip]
        t_i   = ti(t)
        stack_s = str(stack)

        if t_i < 0:
            print(f"{stack_s:<22} {''.join(buf[ip:]):<14} ERROR (bad symbol)")
            print("=> REJECTED"); return

        a = action[state][t_i]
        print(f"{stack_s:<22} {''.join(buf[ip:]):<14} ", end='')

        if a is None:
            print("ERROR\n=> REJECTED"); return
        if a == ACC:
            print("ACCEPT\n=> ACCEPTED"); return
        if a[0] == 's':
            nxt = int(a[1:])
            print(f"Shift {nxt}")
            stack.append(nxt); ip += 1
        else:  # reduce
            p = int(a[1:])
            lhs, rhs = PRODS[p]
            pop_n = 0 if rhs == '#' else len(rhs)
            print(f"Reduce r{p} ({lhs}->{'ε' if rhs=='#' else rhs})")
            for _ in range(pop_n): stack.pop()
            g = go_nt[stack[-1]][ni(lhs)]
            if g < 0:
                print("=> REJECTED (goto error)"); return
            stack.append(g)

# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("Grammar:")
    for lhs, rhs in PRODS[1:]:
        print(f"  {lhs} -> {'epsilon' if rhs == '#' else rhs}")

    FIRST  = compute_first()
    FOLLOW = compute_follow(FIRST)
    states, trans     = build_automaton()
    action, go_nt, conflict = build_slr(states, trans, FIRST, FOLLOW)

    print_sets(FIRST, FOLLOW)
    print_table(action, go_nt, len(states))

    if conflict:
        print("\nConflict(s) found — NOT SLR(1).")
    else:
        print("\nNo conflicts — Grammar is SLR(1).")

    inp = input("\nEnter input string: ").strip()
    parse(action, go_nt, inp)

if __name__ == "__main__":
    main()
