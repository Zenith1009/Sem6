# Lab 1 — String Recognizer for patterns b+a* and a*b+a*

def recognize_pattern1(s):
    """Pattern: b+a*  (one or more b's followed by zero or more a's)"""
    i = 0
    b_count = 0
    while i < len(s) and s[i] == 'b':
        b_count += 1
        i += 1
    if b_count == 0:
        return False
    while i < len(s) and s[i] == 'a':
        i += 1
    return i == len(s)

def recognize_pattern2(s):
    """Pattern: a*b+a*  (zero or more a's, one or more b's, zero or more a's)"""
    i = 0
    while i < len(s) and s[i] == 'a':
        i += 1
    b_count = 0
    while i < len(s) and s[i] == 'b':
        b_count += 1
        i += 1
    if b_count == 0:
        return False
    while i < len(s) and s[i] == 'a':
        i += 1
    return i == len(s)

def main():
    s = input("Enter a string: ").strip()
    print("\nPattern Recognition Results:")
    print("-----------------------------")
    print("Pattern 'b+a*':", "ACCEPTED" if recognize_pattern1(s) else "REJECTED")
    print("Pattern 'a*b+a*':", "ACCEPTED" if recognize_pattern2(s) else "REJECTED")

if __name__ == "__main__":
    main()
