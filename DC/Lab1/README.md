# Distributed Computing — Assignment 1 Reference

This guide summarizes what each required Linux/Unix command does, plus common options you can cite in a viva. Commands are grouped by category and assume a Debian/Ubuntu-like system (adjust package manager flags for other distros).

## Basic commands
- **ls** — list directory contents. Flags: `-l` (long list), `-a` (hidden), `-h` (human sizes), `-t` (time sort), `-R` (recursive).
- **date** — show/set system date. Flags: `+%F` (YYYY-MM-DD), `+%T` (HH:MM:SS), `-u` (UTC), `-R` (RFC 2822), `-Iseconds` (ISO-8601 with seconds).
- **help** — shell built-in help for Bash built-ins (e.g., `help cd`). Flags: `-m` (more verbose help), `-s` (short synopsis).
- **info** — read GNU Info manuals. Usage: `info coreutils ls`, navigation with `n`/`p`.
- **man** — read manual pages. Flags: `-k` (keyword search), `-f` (whatis), section numbers (e.g., `man 5 passwd`).
- **who** — show logged-in users. Flags: `-a` (all details), `-b` (last boot), `-H` (headers).
- **pwd** — print working directory. Flags: `-L` (logical, default), `-P` (physical, resolves symlinks).
- **cat** — concatenate/print files. Flags: `-n` (number lines), `-b` (number non-blank), `-A` (show control chars), `-E` (show line ends), `-s` (squeeze blank lines).
- **more** — pager to view text one screen at a time. Flags: `-d` (helpful prompts), `-c` (paint from top), `-p` (clear-and-paint), `+n` (start at line n).
- **mv** — move/rename files. Flags: `-i` (prompt), `-n` (no overwrite), `-v` (verbose), `-f` (force), `-u` (update if newer).
- **rm** — remove files. Flags: `-i` (prompt), `-r`/`-R` (recursive), `-f` (force), `-v` (verbose).
- **chmod** — change permissions. Modes: symbolic (`u+rx`, `g-w`, `o=r`) or octal (`755`). Flags: `-R` (recursive), `--reference=FILE` (copy perms).
- **whoami** — print current user name.
- **logout** — exit a login shell.
- **wc** — word/line/byte counts. Flags: `-l` (lines), `-w` (words), `-c` (bytes), `-m` (chars), `-L` (max line length).
- **grep** — search patterns. Flags: `-i` (ignore case), `-r` (recursive), `-n` (line numbers), `-E` (extended regex), `-v` (invert match), `-A/-B/-C` (context).
- **sort** — sort lines. Flags: `-n` (numeric), `-r` (reverse), `-k` (key/field), `-u` (unique), `-t` (delimiter), `-h` (human numbers).
- **mkdir** — make directories. Flags: `-p` (parents), `-v` (verbose), `-m` (mode).
- **rmdir** — remove empty directories. Flags: `-p` (parents), `-v` (verbose).
- **cd** — change directory. Options: `cd -` (previous), `cd ~` (home), `cd ..` (parent), `CDPATH` environment for search paths.
- **tail** — view file end. Flags: `-n` (lines), `-f` (follow), `-c` (bytes), `-F` (follow with reopen on rotate).
- **cmp** — byte-wise compare two files. Flags: `-l` (show byte diffs), `-s` (silent status), `-n N` (compare first N bytes).
- **diff** — line-wise diff. Flags: `-u` (unified), `-r` (recursive), `-q` (brief), `-y` (side-by-side), `--color=auto`.
- **cp** — copy files. Flags: `-r`/`-R` (recursive), `-p` (preserve mode/owner/timestamps), `-a` (archive = -p -d -r), `-u` (only if newer), `-i` (prompt), `-v` (verbose).
- **clear** — clear terminal screen.
- **df** — filesystem disk usage. Flags: `-h` (human), `-T` (type), `-i` (inodes), `-P` (POSIX format), `--total` (summary).
- **du** — per-directory disk usage. Flags: `-h` (human), `-s` (summary), `-d N` (depth), `-c` (grand total), `--apparent-size`.
- **uname** — system info. Flags: `-a` (all), `-r` (kernel release), `-s` (kernel name), `-m` (machine), `-n` (nodename).
- **apt-get** — Debian package tool. Subcommands: `update`, `upgrade`, `install pkg`, `remove pkg`, `autoremove`, `clean`. Flags: `-y` (assume yes), `-s` (simulate), `--download-only`.
- **find** — search filesystem. Flags: `-name/-iname`, `-type f/d`, `-mtime/-mmin`, `-size`, `-maxdepth`, `-exec ... {} \;`, `-print0` (for xargs -0).
- **wget** — non-interactive downloader. Flags: `-O file` (output), `-c` (continue), `-r` (recursive), `-l N` (depth), `--limit-rate`, `--user`/`--password` (auth).
- **top** — interactive process monitor. Useful keys: `P` (sort CPU), `M` (sort memory), `k` (kill), `r` (renice), `1` (per-CPU), `q` (quit). Options: `-b` (batch), `-n` (iterations).
- **mpstat** (listed as mpstate) — per-CPU statistics from sysstat. Flags: `-P ALL` (all CPUs), `interval count` (sampling), `-u` (CPU usage), `-I SUM` (interrupts).
- **netstat** — network connections/routes. Flags: `-t` (TCP), `-u` (UDP), `-l` (listening), `-p` (process), `-n` (numeric), `-r` (routes), `-s` (stats).
- **sar** — system activity report (sysstat). Flags: `-u` (CPU), `-r` (memory), `-n DEV` (net I/O), `-d` (disks), `interval count` sampling.
- **chown** — change file owner/group. Usage: `chown user file`, `chown user:group file`, flags: `-R` (recursive), `--reference=FILE`.

## Process-related commands
- **ps** — snapshot processes. Flags: `aux` (BSD style all), `-ef` (full format), `-o pid,cmd` (custom columns), `--sort=-%cpu`.
- **kill** — send signals by PID. Signals: `-15` (TERM), `-9` (KILL), `-HUP`, `-INT`. Flag: `-l` (list signals), `-s SIG` (name), `-- -1234` (negative for process groups).
- **Background processing (&)** — append `&` to run in background. Use `jobs` to list, `fg %1` to foreground, `bg %1` to resume stopped jobs.
