# Lab 6 — Recursive Descent Parser (extended: supports identifiers only, not numbers)
# Grammar:
#   E  -> T E'
#   E' -> + T E' | @   (@ = epsilon)
#   T  -> F T'
#   T' -> * F T' | @
#   F  -> id | ( E )

class RDP:
    def __init__(self, text):
        self.inp = text.replace(' ', '').replace('\t', '')
        self.pos = 0
        self.error = False

    def peek(self):
        return self.inp[self.pos] if self.pos < len(self.inp) else '\0'

    def E(self):
        if self.error: return
        self.T()
        self.E_prime()

    def E_prime(self):
        if self.error: return
        if self.peek() == '+':
            self.pos += 1
            self.T()
            self.E_prime()

    def T(self):
        if self.error: return
        self.F()
        self.T_prime()

    def T_prime(self):
        if self.error: return
        if self.peek() == '*':
            self.pos += 1
            self.F()
            self.T_prime()

    def F(self):
        if self.error: return
        ch = self.peek()
        if ch == '(':
            self.pos += 1
            self.E()
            if self.peek() == ')':
                self.pos += 1
            else:
                self.error = True
        elif ch.isalpha():
            while self.pos < len(self.inp) and self.inp[self.pos].isalnum():
                self.pos += 1
        else:
            self.error = True

    def parse(self):
        self.E()
        return not self.error and self.pos == len(self.inp)

def main():
    print("Grammar:")
    print("E  -> T E'")
    print("E' -> + T E' | @")
    print("T  -> F T'")
    print("T' -> * F T' | @")
    print("F  -> id | (E)\n")

    s = input("Enter string: ").strip()
    parser = RDP(s)
    print("Accepted" if parser.parse() else "Rejected")

if __name__ == "__main__":
    main()
