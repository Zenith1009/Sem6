# Lab 10 Part 2 — LALR(1) Parser
# Grammar: S → AA,  A → aA | b
# Shows parser moves for "aaabb"

prods = [("S'",("S",)), ("S",("A","A")), ("A",("a","A")), ("A",("b",))]
NTS   = {p[0] for p in prods}

def first_of(seq, F):
    out = set()
    for s in seq:
        f = F.get(s, {s})
        out |= f - {"e"}
        if "e" not in f: return out
    return out | {"e"}

def compute_first():
    F = {l: set() for l,_ in prods}
    ch = True
    while ch:
        ch = False
        for l,r in prods:
            f = first_of(r, F)
            if not f <= F[l]: F[l] |= f; ch = True
    return F

def closure(I, F):
    S = set(I)
    ch = True
    while ch:
        ch = False
        for p,d,a in list(S):
            rhs = prods[p][1]
            if d < len(rhs) and rhs[d] in NTS:
                for la in first_of(rhs[d+1:]+(a,), F) - {"e"}:
                    for i,(l,_) in enumerate(prods):
                        if l == rhs[d] and (i,0,la) not in S:
                            S.add((i,0,la)); ch = True
    return frozenset(S)

def goto(I, x, F):
    moved = {(p,d+1,a) for p,d,a in I if d < len(prods[p][1]) and prods[p][1][d] == x}
    return closure(moved, F) if moved else frozenset()

def build_lr1(F):
    s0 = closure({(0,0,"$")}, F)
    states, idx, trans = [s0], {s0: 0}, {}
    i = 0
    while i < len(states):
        for x in {prods[p][1][d] for p,d,_ in states[i] if d < len(prods[p][1])}:
            g = goto(states[i], x, F)
            if g not in idx: idx[g] = len(states); states.append(g)
            trans[(i,x)] = idx[g]
        i += 1
    return states, trans

def merge(states, trans):
    core = lambda s: frozenset((p,d) for p,d,_ in s)
    cm, new, o2n = {}, [], {}
    for i,s in enumerate(states):
        c = core(s)
        if c not in cm: cm[c] = len(new); new.append(set(s))
        else: new[cm[c]] |= set(s)
        o2n[i] = cm[c]
    merged  = [frozenset(s) for s in new]
    m_trans = {(o2n[i],x): o2n[j] for (i,x),j in trans.items()}
    return merged, m_trans

def build(F):
    states, trans = build_lr1(F)
    states, trans = merge(states, trans)
    act, go = {}, {}
    for i,st in enumerate(states):
        for p,d,a in st:
            rhs = prods[p][1]
            if d < len(rhs):
                if rhs[d] not in NTS: act[(i,rhs[d])] = ("s", trans[(i,rhs[d])])
            else:
                if p == 0: act[(i,"$")] = ("acc",)
                else:      act[(i,a)]   = ("r", p)
        for (i2,x),ns in trans.items():
            if i2 == i and x in NTS: go[(i,x)] = ns
    return states, act, go

def print_table(states, act, go):
    terms = ["a","b","$"]; nts = ["S","A"]
    print(f"\n{'St':>3} |" + "".join(f"{t:>6}" for t in terms) + " |" + "".join(f"{n:>5}" for n in nts))
    print("-" * 36)
    for i in range(len(states)):
        a_cells = "".join(f"{'acc' if (a:=act.get((i,t))) and a[0]=='acc' else (a[0]+str(a[1]) if a else '-'):>6}" for t in terms)
        g_cells = "".join(f"{go.get((i,n),'-'):>5}" for n in nts)
        print(f"{i:>3} |{a_cells} |{g_cells}")

def parse(act, go, s):
    buf = list(s) + ["$"]; stk = [0]; ip = 0
    print(f"\n{'Stack':<28} {'Input':<12} Action")
    print("-" * 54)
    while True:
        t = buf[ip]; a = act.get((stk[-1], t))
        print(f"{str(stk):<28} {''.join(buf[ip:]):<12}", end=" ")
        if not a:     print("ERROR\n=> REJECTED"); return
        if a[0]=="s": print(f"Shift {a[1]}"); stk.append(a[1]); ip += 1
        elif a[0]=="r":
            l,r = prods[a[1]]; print(f"Reduce r{a[1]} ({l}->{''.join(r)})")
            for _ in r: stk.pop()
            stk.append(go[(stk[-1], l)])
        else:         print("Accept\n=> ACCEPTED"); return

F = compute_first()
states, act, go = build(F)
print("LALR(1) | Grammar: S -> AA,  A -> aA | b")
print(f"States: {len(states)}  (merged from LR(1) collection)")
print(f"FIRST(S)={sorted(F['S'])}  FIRST(A)={sorted(F['A'])}")
print_table(states, act, go)

s = input("\nEnter input string (Enter to skip): ").strip()
if s: parse(act, go, s)
