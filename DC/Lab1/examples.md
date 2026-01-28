# Command Examples and Runs

Sample invocations with representative outputs (trimmed). Adapt paths and URLs as needed.

## Basic commands

### ls
```
ls -alh                     # all files incl dotfiles, long listing, human sizes
ls -ltr                     # long list, sort by time (oldest last), reverse
ls /var/log                 # list contents of /var/log
ls -R src                   # recurse through src/
ls --color=auto             # colorized output (GNU ls)
```

### date
```
date                         # current local date/time
date -u                      # show in UTC
date +%F_%H-%M-%S            # custom YYYY-MM-DD_HH-MM-SS format
date -R                      # RFC 2822 format
date -Iseconds               # ISO 8601 with seconds (GNU date)
```

### help / info / man
```
help cd                      # bash built-in help for cd
help -m pushd                # verbose help entry for pushd
info coreutils ls            # open GNU info page for ls
man 5 passwd                 # man section 5 (file formats) for passwd
man -k network               # search man page keywords containing "network"
```

### who / whoami / logout
```
who -a                       # all login info and terminals
who -b                       # last system boot time
whoami                       # current user name
logout                       # ends login shell session
```

### pwd / cd
```
pwd                          # print working directory
cd /tmp && pwd               # change to /tmp then show it
cd -                         # jump back to previous directory
```

### cat / more
```
cat -n README.md             # show file with line numbers
cat -A /etc/hosts            # show control chars and line ends
more -d README.md            # paginate with helpful prompts
more +20 README.md           # start display at line 20
```

### mv / cp / rm / mkdir / rmdir
```
mv -i old.txt archive/old.txt # move/rename with prompt before overwrite
mv -v file{1,2}.txt backup/   # move multiple files verbosely
cp -av src/ dest/             # archive copy (preserve attrs, recurse)
cp -u notes.txt backup/       # copy only if source is newer
rm -i temp.txt                # remove with confirmation
rm -rf build/                 # force-recursive delete directory
mkdir -p data/raw             # create nested directories if missing
rmdir -pv empty/child         # remove empty dir, verbose, include parents
```

### chmod / chown
```
chmod 644 report.txt          # set perms rw-r--r--
chmod -R u+rx scripts/        # add read/execute for user recursively
chown alice:dev report.txt    # change owner to alice, group dev
chown -R www-data:www-data /var/www # change owner/group recursively (sudo)
```

### wc / grep / sort
```
wc -l *.c                    # line counts for all .c files
wc -w essay.txt              # word count of file
grep -rin "error" logs/      # recursive, case-insensitive search with lines
grep -E "(WARN|ERROR)" app.log # extended regex match for WARN or ERROR
sort -h sizes.txt            # sort human-size numbers (GNU)
sort -t, -k2,2n data.csv     # CSV: sort by 2nd field numeric
```

### tail
```
tail -n 15 app.log            # last 15 lines
tail -f /var/log/syslog       # follow new lines as they append
tail -c 200 notes.txt         # last 200 bytes
tail -F rotated.log           # follow and reopen if file is rotated
```

### cmp / diff
```
cmp fileA.bin fileB.bin       # compare binary files, report first diff
cmp -l a.bin b.bin | head     # list differing bytes (first few shown)
diff -u old.c new.c            # unified diff between text files
diff -r configs.old configs.new # recursive diff of directories
```

### clear
```
clear                        # clear terminal screen
printf "\033c"               # send reset/clear escape sequence
```

### df / du
```
df -h                        # disk usage per filesystem, human units
df -i                        # inode usage per filesystem
du -sh .                      # total size of current dir
du -h --max-depth=1 /var/log # per-subdir sizes depth 1 (GNU)
du -ch ~/projects            # sizes with cumulative total (GNU)
```

### uname
```
uname -a                     # all system info
uname -r                     # kernel release version
uname -m                     # hardware architecture
```

### apt-get
```
sudo apt-get update          # refresh package lists
sudo apt-get install htop -y # install htop non-interactively
sudo apt-get remove htop     # remove package
sudo apt-get autoremove      # clean unused deps
sudo apt-get clean           # clear package cache
```

### find
```
find . -maxdepth 2 -type f -name "*.c"       # find C files within depth 2
find /var/log -type f -mtime -1               # files modified in last day
find . -size +10M -print0 | xargs -0 ls -lh   # list large files with details
find . -type f -exec chmod 644 {} \;          # set perms on all files
find /tmp -type f -mmin +60 -delete           # delete temp files older than 60 min
```

### wget
```
wget https://example.com/file.tar.gz          # download file to current dir
wget -O index.html https://example.com/        # save as custom filename
wget -c http://releases.ubuntu.com/iso         # continue partial download
wget -r -l2 https://example.org/docs/          # recursive download depth 2
wget --limit-rate=200k https://example.com/large.bin # throttle download speed
```

### top
```
top                           # interactive process monitor
TOP_BATCH=yes top -b -n 1      # one-shot batch output (GNU top)
```
Interactive keys: P (CPU sort), M (mem sort), k (kill PID), r (renice), 1 (per-CPU), q (quit).

### mpstat (mpstate in list)
```
mpstat 2 5                    # CPU stats every 2s, 5 samples
mpstat -P ALL 1 3             # per-CPU stats every 1s, 3 samples
mpstat -I SUM 1 2             # interrupt summary every 1s, 2 samples
```

### netstat
```
netstat -tulpn               # TCP/UDP listening with PIDs (Linux)
netstat -an | head           # first lines of all sockets numeric
netstat -rn                  # routing table numeric
netstat -s                   # protocol statistics summary
```

### sar
```
sar -u 1 5                   # CPU usage every 1s, 5 samples
sar -r 1 3                   # memory stats every 1s, 3 samples
sar -n DEV 1 3               # network device stats every 1s, 3 samples
sar -d 1 3                   # disk stats every 1s, 3 samples
```

## Process-related commands

### ps
```
ps aux | head                # snapshot of processes (BSD style), first few lines
ps -ef --sort=-%cpu | head   # full-format, sorted by CPU desc (GNU ps)
ps -o pid,ppid,cmd -C sshd   # only pid, ppid, cmd for processes named sshd
ps -p 1,2,3 -o pid,cmd       # show pid and command for specific PIDs
```

### kill
```
kill -l                      # list all signal names/numbers
kill -TERM 1234              # request graceful stop of PID 1234
kill -9 2345                 # force kill PID 2345
kill -HUP $(pidof nginx)     # send HUP (reload) to nginx master
kill -- -1234                # send signal to process group 1234
```

### Background jobs (&)
```
sleep 60 &                   # run sleep in background
long_task.sh --verbose &     # start long script in background
jobs                         # list background jobs
bg %1                        # resume job 1 in background
fg %1                        # bring job 1 to foreground
```

### Extra combos
```
grep -rin "TODO" . | sort > todos.txt          # find TODOs, sort, save
find . -type f -name "*.log" -mtime +7 -exec rm {} \; # delete logs older than 7 days
ps aux | grep python | grep -v grep             # list python processes (filter out grep)
sudo kill -TERM $(pgrep -f "gunicorn")         # gracefully stop gunicorn processes
```
