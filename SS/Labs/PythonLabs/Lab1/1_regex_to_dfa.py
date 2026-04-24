# Lab 1 — Regex to DFA (linear regex: literals, *, +)

transitions = []
final_state = 0

def build_dfa(re):
    global transitions, final_state
    transitions = []
    cur = 0
    i = 0
    while i < len(re):
        ch = re[i]
        nxt = re[i + 1] if i + 1 < len(re) else '\0'

        if ch in ('*', '+', '|'):
            i += 1
            continue

        if nxt == '*':
            transitions.append((cur, ch, cur))
            i += 2
        elif nxt == '+':
            transitions.append((cur, ch, cur + 1))
            transitions.append((cur + 1, ch, cur + 1))
            cur += 1
            i += 2
        else:
            transitions.append((cur, ch, cur + 1))
            cur += 1
            i += 1

    final_state = cur

def validate(s):
    state = 0
    for ch in s:
        moved = False
        for (frm, sym, to) in transitions:
            if frm == state and sym == ch:
                state = to
                moved = True
                break
        if not moved:
            return False
    return state == final_state

def print_dfa():
    print("\nDFA")
    print(f"{'State':<8} {'Input':<8} {'Next':<8}")
    print("-" * 24)
    for (frm, sym, to) in transitions:
        print(f"q{frm:<7} {sym:<8} q{to:<7}")
    print("-" * 24)
    print(f"Start: q0\nFinal: q{final_state}")

def main():
    re = input("Enter regex: ").strip()
    build_dfa(re)
    print_dfa()

    while True:
        c = input("\nTest a string? (y/n): ").strip().lower()
        if c == 'y':
            s = input("String: ").strip()
            print("ACCEPTED" if validate(s) else "REJECTED")
        else:
            break

if __name__ == "__main__":
    main()
