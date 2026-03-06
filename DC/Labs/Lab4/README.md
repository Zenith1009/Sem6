# Distributed Computing (CS332) | Assignment 4
## RPC Simulation (C + SunRPC in Docker)

---

**Student Name :** *Naishadh Rana* <br>
**Roll. No :** U23CS014

---

## Assignment Requirement
Simulate RPC by creating procedures on a remote machine and calling them from a local machine.

Programs implemented:
1. Factorial of a given number
2. Calculator (basic operations)
3. Prime check
4. Fibonacci series up to a given number
5. Maximum in an integer array

---

## Step 1: Verify `rpcbind` installation

```bash
$ rpcinfo
```

---

## Step 2: Install `rpcbind` (if needed)

```bash
$ sudo apt-get update
$ sudo apt-get install rpcbind
```

In this lab, these packages are installed through Docker image setup.

---

## Step 3: Create IDL file

IDL file used: `add.x`

---

## Step 4: Compile IDL file using `rpcgen`

```bash
$ rpcgen -a -C add.x
```

Generated files:
- `add.h`
- `add_client.c`
- `add_clnt.c`
- `add_server.c`
- `add_svc.c`
- `add_xdr.c`
- `Makefile.add`

---

## Step 5: Edit server and client programs

Edited files:
- `add_server.c` (all 5 RPC procedures)
- `add_client.c` (menu-driven caller)

---

## Step 6: Compile and run

```bash
$ make -f Makefile.add
```

Run server (terminal 1):

```bash
$ ./add_server
```

Run client (terminal 2):

```bash
$ ./add_client localhost
```

---

## Docker setup used on macOS

Build Docker image:

```bash
docker build -t dc-lab4-rpc .
```

Start container:

```bash
docker run -d --name dc-lab4-rpc-run -v "$PWD":/work -w /work dc-lab4-rpc sleep infinity
```

Inside container (generation + build + server):

```bash
docker exec dc-lab4-rpc-run bash -lc "rpcgen -a -C add.x"
docker exec dc-lab4-rpc-run bash -lc "make -f Makefile.add"
docker exec dc-lab4-rpc-run bash -lc "rpcbind || true; ./add_server"
```

Client from second terminal:

```bash
docker exec -it dc-lab4-rpc-run bash
cd /work
./add_client localhost
```

### Container reuse and conflict notes

If you see:

```text
Conflict. The container name "/dc-lab4-rpc-run" is already in use
```

use one of these options:

1. Reuse existing container:

```bash
docker start dc-lab4-rpc-run
docker exec -it dc-lab4-rpc-run bash
```

2. Remove old container and create a new one with same name:

```bash
docker rm -f dc-lab4-rpc-run
docker run -d --name dc-lab4-rpc-run -v "$PWD":/work -w /work dc-lab4-rpc sleep infinity
```

Important:
- `docker rm -f dc-lab4-rpc-run` removes only the container instance.
- It does **not** remove your image (`dc-lab4-rpc`) or your code files in the host folder.

---

## Verified Output (executed)

```text
===== RPC MENU =====
1. Find factorial
2. Calculator (basic operations)
3. Prime check
4. Fibonacci series up to n
5. Maximum in integer array
6. Exit
Enter your choice: Enter number: Result: 120

Enter your choice: Enter first number: Enter second number: Operation (1=ADD, 2=SUB, 3=MUL, 4=DIV): Result: 35.0000

Enter your choice: Enter number: Result: Prime

Enter your choice: Enter upper limit: Result: 0,1,1,2,3,5,8,13

Enter your choice: Enter comma-separated integers: Result: 99
```

---

## Conclusion
Assignment 4 is completed exactly in C using SunRPC (`rpcgen`, `rpcbind`, generated stubs/skeleton), executed in Docker for macOS compatibility.


## Other stuff:


## Docker commands used instead:

Build image:

```bash
docker build -t dc-lab4-rpc .
```

Run container:

```bash
docker run -d --name dc-lab4-rpc-run -v "$PWD":/work -w /work dc-lab4-rpc sleep infinity
```

Generate and compile inside container:

```bash
docker exec dc-lab4-rpc-run bash -lc "rpcgen -a -C add.x"
docker exec dc-lab4-rpc-run bash -lc "make -f Makefile.add"
```

Start rpcbind and server:

```bash
docker exec dc-lab4-rpc-run bash -lc "rpcbind || true; ./add_server"
```

Client from another terminal:

```bash
docker exec -it dc-lab4-rpc-run bash
cd /work
./add_client localhost
```
