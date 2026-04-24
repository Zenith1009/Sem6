# Lab 7 — LR(0) Parser
# Grammar:
#   (1) E -> T T
#   (2) T -> a T
#   (3) T -> b

prods   = [None, ('E', 'TT'), ('T', 'aT'), ('T', 'b')]
rhs_len = [0,    2,            2,            1]

# LR(0) ACTION table: 'sX' = shift to X, 'rY' = reduce by Y, 'acc', '-' = error
action = [
    #  a      b      $
    ['s3',  's4',  '-'  ],   # 0
    ['-',   '-',   'acc'],   # 1
    ['s3',  's4',  '-'  ],   # 2
    ['s3',  's4',  '-'  ],   # 3
    ['r3',  'r3',  'r3' ],   # 4
    ['r1',  'r1',  'r1' ],   # 5
    ['r2',  'r2',  'r2' ],   # 6
]

# GOTO[state][E=0, T=1]
gotos = [
    [1, 2], [-1, -1], [-1, 5], [-1, 6],
    [-1, -1], [-1, -1], [-1, -1]
]

TERMS    = ['a', 'b', '$']
NONTERMS = ['E', 'T']

def term_idx(c):
    if c == 'a':  return 0
    if c == 'b':  return 1
    if c in ('$', ''): return 2
    return -1

def nonterm_idx(c):
    if c == 'E': return 0
    if c == 'T': return 1
    return -1

def print_table():
    print("\nLR(0) Parse Table")
    print("State |   a   b   $  ||  E   T")
    print("--------------------------------")
    for i, row in enumerate(action):
        g = gotos[i]
        ge = str(g[0]) if g[0] >= 0 else '-'
        gt = str(g[1]) if g[1] >= 0 else '-'
        print(f"  {i}   | {row[0]:<3} {row[1]:<3} {row[2]:<3} || {ge:<3} {gt}")

def parse(raw):
    inp = raw + '$'
    st   = [0]
    sym  = ['#']
    ip   = 0
    step = 1

    print(f'\nParser Moves (LR(0)) for input "{raw}"')
    print(f"{'Step':<5} {'Stack':<27} {'Input':<10} Action")
    print("-" * 60)

    while True:
        state = st[-1]
        t     = inp[ip] if ip < len(inp) else '$'
        ti    = term_idx(t)
        stack_view = ' '.join(str(x) for x in st)

        if ti < 0:
            print(f"{step:<5} {stack_view:<27} {inp[ip:]:<10} error (invalid symbol)")
            return False

        act = action[state][ti]
        print(f"{step:<5} {stack_view:<27} {inp[ip:]:<10} ", end='')

        if act[0] == 's':
            nxt = int(act[1:])
            print(f"shift {nxt}")
            st.append(nxt)
            sym.append(t)
            ip += 1
        elif act[0] == 'r':
            p = int(act[1:])
            lhs, _ = prods[p]
            print(f"reduce {lhs} -> {''.join(prods[p][1])}")
            for _ in range(rhs_len[p]):
                st.pop(); sym.pop()
            g = gotos[st[-1]][nonterm_idx(lhs)]
            if g < 0:
                print("error (goto)")
                return False
            st.append(g)
            sym.append(lhs)
        elif act == 'acc':
            print("accept")
            return True
        else:
            print("error")
            return False
        step += 1

def main():
    print("Grammar:")
    print("E -> T T")
    print("T -> a T | b")
    print_table()
    raw = input("\nEnter input string over {a,b}: ").strip()
    print("\nResult:", "Accepted" if parse(raw) else "Rejected")

if __name__ == "__main__":
    main()
