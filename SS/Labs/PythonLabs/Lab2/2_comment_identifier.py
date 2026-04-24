# Lab 2 — Comment Identifier
# Checks whether a given line is a comment (single-line // or multi-line /* */)

def identify_comment(line):
    stripped = line.lstrip()

    if stripped.startswith('//'):
        return "Single-line comment"
    elif stripped.startswith('/*'):
        if '*/' in stripped:
            return "Multi-line comment (complete)"
        else:
            return "Multi-line comment START"
    elif '*/' in line:
        return "Multi-line comment END"
    else:
        return "NOT a comment"

def main():
    line = input("Enter a line: ")
    print("Result:", identify_comment(line))

if __name__ == "__main__":
    main()
