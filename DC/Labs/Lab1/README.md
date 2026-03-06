# Distributed Computing (CS332) | Assignment 1
## **Linux/Unix Commands**

---

**Student Name :** *Naishadh Rana* <br>
**Roll. No :** U23CS014

---

---

## 1. File & Directory Operations

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `ls` | List directory contents | `-l` (long), `-a` (hidden), `-h` (human sizes), `-R` (recursive) |
| `cd` | Change directory | `cd -` (previous), `cd ~` (home), `cd ..` (parent) |
| `pwd` | Print working directory | `-P` (physical, resolves symlinks) |
| `mkdir` | Create directory | `-p` (create parents), `-m` (set mode) |
| `rmdir` | Remove empty directory | `-p` (remove parents too) |
| `cp` | Copy files | `-r` (recursive), `-p` (preserve attributes), `-i` (prompt) |
| `mv` | Move/rename files | `-i` (prompt), `-n` (no overwrite), `-u` (update if newer) |
| `rm` | Remove files | `-r` (recursive), `-f` (force), `-i` (prompt) |
| `cat` | Display file contents | `-n` (number lines), `-A` (show control chars) |
| `more` | Pager (one screen at a time) | `-d` (helpful prompts), `+n` (start at line n) |
| `tail` | View end of file | `-n` (lines), `-f` (follow live) |

### Viva Prep
- **Q: Difference between `rm` and `rmdir`?**  
  A: `rmdir` removes only empty directories; `rm -r` removes directories with contents.
- **Q: What does `cp -a` do?**  
  A: Archive mode = `-p -d -r` (preserve all attributes, copy symlinks as links, recursive).
- **Q: How to go to previous directory?**  
  A: `cd -`

---

## 2. File Permissions

| Command | Purpose | Usage |
|---------|---------|-------|
| `chmod` | Change permissions | Symbolic: `chmod u+x file`, Octal: `chmod 755 file` |
| `chown` | Change owner/group | `chown user:group file`, `-R` (recursive) |

### Permission Bits
```
r = 4 (read)
w = 2 (write)
x = 1 (execute)

Example: 755 = rwxr-xr-x (owner: all, group/others: read+execute)
```

### Viva Prep
- **Q: What does `chmod 644` mean?**  
  A: Owner can read/write (6), group and others can only read (4).
- **Q: Difference between `chmod` and `chown`?**  
  A: `chmod` changes permissions (rwx); `chown` changes ownership (user/group).

---

## 3. Text Processing

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `wc` | Count lines/words/bytes | `-l` (lines), `-w` (words), `-c` (bytes) |
| `grep` | Search patterns | `-i` (ignore case), `-r` (recursive), `-n` (line numbers), `-v` (invert) |
| `sort` | Sort lines | `-n` (numeric), `-r` (reverse), `-u` (unique) |
| `diff` | Compare files line by line | `-u` (unified), `-q` (brief) |
| `cmp` | Compare files byte by byte | `-s` (silent, exit status only) |

### Viva Prep
- **Q: Difference between `diff` and `cmp`?**  
  A: `diff` compares line-by-line (text); `cmp` compares byte-by-byte (binary).
- **Q: How to count only lines in a file?**  
  A: `wc -l filename`
- **Q: How to search recursively for a pattern?**  
  A: `grep -r "pattern" directory/`

---

## 4. System Information

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `uname` | System/kernel info | `-a` (all), `-r` (kernel release), `-m` (machine) |
| `whoami` | Print current username | — |
| `who` | Show logged-in users | `-a` (all details), `-b` (last boot) |
| `date` | Show/set date/time | `+%F` (YYYY-MM-DD), `+%T` (HH:MM:SS), `-u` (UTC) |
| `df` | Disk space usage | `-h` (human readable), `-T` (filesystem type) |
| `du` | Directory disk usage | `-h` (human), `-s` (summary), `-d N` (depth) |

### Viva Prep
- **Q: Difference between `df` and `du`?**  
  A: `df` shows filesystem-level usage; `du` shows per-directory usage.
- **Q: How to get kernel version?**  
  A: `uname -r`

---

## 5. Process Management

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `ps` | Snapshot of processes | `aux` (all users), `-ef` (full format), `-o` (custom columns) |
| `top` | Interactive process monitor | `P` (sort by CPU), `M` (sort by memory), `k` (kill) |
| `kill` | Send signal to process | `-9` (SIGKILL), `-15` (SIGTERM), `-l` (list signals) |
| `&` | Run command in background | `command &`, use `jobs` to list, `fg` to foreground |

### Viva Prep
- **Q: Difference between `kill -9` and `kill -15`?**  
  A: `-15` (TERM) asks process to terminate gracefully; `-9` (KILL) forces immediate termination.
- **Q: How to see all processes?**  
  A: `ps aux` or `ps -ef`
- **Q: How to run a process in background?**  
  A: Append `&` to the command (e.g., `./script.sh &`)

---

## 6. Network & Monitoring

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `netstat` | Network connections | `-t` (TCP), `-u` (UDP), `-l` (listening), `-p` (process), `-n` (numeric) |
| `wget` | Download files | `-O` (output file), `-c` (continue), `-r` (recursive) |
| `sar` | System activity report | `-u` (CPU), `-r` (memory), `-n DEV` (network) |
| `mpstat` | Per-CPU statistics | `-P ALL` (all CPUs) |

### Viva Prep
- **Q: How to see listening ports?**  
  A: `netstat -tuln`
- **Q: How to resume a download?**  
  A: `wget -c URL`

---

## 7. Help & Documentation

| Command | Purpose | Usage |
|---------|---------|-------|
| `man` | Manual pages | `man ls`, `man -k keyword` (search) |
| `info` | GNU Info docs | `info coreutils` |
| `help` | Bash built-in help | `help cd` |

### Viva Prep
- **Q: Difference between `man` and `info`?**  
  A: `man` shows traditional Unix manuals; `info` shows GNU hypertext documentation (more detailed for GNU tools).

---

## 8. Miscellaneous

| Command | Purpose |
|---------|---------|
| `clear` | Clear terminal screen |
| `logout` | Exit login shell |
| `find` | Search filesystem (`find . -name "*.txt"`) |
| `apt-get` | Package manager (Debian/Ubuntu) |

### Find Examples
```bash
find . -name "*.java"           # Find by name
find . -type d                  # Find directories only
find . -mtime -7                # Modified in last 7 days
find . -size +10M               # Larger than 10MB
```

---

## Quick Reference: Common Tasks

| Task | Command |
|------|---------|
| List all files including hidden | `ls -la` |
| Copy directory recursively | `cp -r src/ dest/` |
| Delete directory with contents | `rm -rf dirname/` |
| Make file executable | `chmod +x script.sh` |
| Find large files | `find . -size +100M` |
| Check disk space | `df -h` |
| Kill process by PID | `kill -9 1234` |
| Download file | `wget URL` |
| Search in files | `grep -r "text" .` |

---

## Key Takeaways
1. Use `-h` flag for human-readable sizes (`df -h`, `du -h`, `ls -lh`).
2. Use `-r` or `-R` for recursive operations on directories.
3. Use `-i` flag for interactive prompts before destructive operations.
4. Permissions: read=4, write=2, execute=1; combine for octal (e.g., 755).
5. Signals: SIGTERM (15) = graceful stop, SIGKILL (9) = force kill.
6. Use `man command` to learn any command's options.
