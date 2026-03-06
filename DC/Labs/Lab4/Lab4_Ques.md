# Assignment 4: RPC Simulation

Simulate RPC by creating procedures on a remote machine and calling them from a local machine.

## List of Programs for RPC

1. Find the factorial of a given number
2. Implement a Calculator (basic operations)
3. Determine whether a given number is prime
4. Print the Fibonacci series up to a given number
5. Find the maximum value in an array of integers using RPC

## Steps to Run RPC Program

### Step 1: Verify rpcbind Installation

Check if rpcbind is installed:
```bash
$ rpcinfo
```

### Step 2: Install rpcbind (if needed)

```bash
$ sudo apt-get update
$ sudo apt-get install rpcbind
```

### Step 3: Create IDL File

Create an IDL file (e.g., `add.x`):
```c
/* IDL file for adding two numbers */
struct numbers {
    int a;
    int b;
};

program ADD_PROG {
    version ADD_VERS {
        int add(numbers) = 1;
    } = 1;
} = 0x4562877;
```

### Step 4: Compile IDL File

```bash
$ rpcgen -a -C add.x
```

Generated files:
- `add.h` - header file
- `add_client.c` - client program
- `add_clnt.c` - client stub
- `add_server.c` - server program
- `add_svc.c` - server skeleton
- `add_xdr.c` - XDR routines
- `Makefile.add` - Makefile

### Step 5: Edit Server and Client Programs

**Edit `add_server.c`:**
```c
#include "add.h"

int *
add_1_svc(numbers *argp, struct svc_req *rqstp)
{
    static int result;
    printf("add(%d,%d) is called\n", argp->a, argp->b);
    result = argp->a + argp->b;
    return &result;
}
```

**Edit `add_client.c`:**
```c
#include "add.h"

void
add_prog_1(char *host, int x, int y)
{
    CLIENT *clnt;
    int *result_1;
    numbers add_1_arg;

    clnt = clnt_create(host, ADD_PROG, ADD_VERS, "udp");
    if (clnt == NULL) {
        clnt_pcreateerror(host);
        exit(1);
    }

    add_1_arg.a = x;
    add_1_arg.b = y;
    result_1 = add_1(&add_1_arg, clnt);
    if (result_1 == (int *) NULL) {
        clnt_perror(clnt, "call failed");
    } else {
        printf("Result: %d\n", *result_1);
    }
    clnt_destroy(clnt);
}

int
main(int argc, char *argv[])
{
    char *host;

    if (argc < 4) {
        printf("usage: %s server_host number1 number2\n", argv[0]);
        exit(1);
    }
    host = argv[1];
    add_prog_1(host, atoi(argv[2]), atoi(argv[3]));
    exit(0);
}
```

### Step 6: Compile and Run

Compile all files:
```bash
$ make -f Makefile.add
```

Run the server (terminal 1):
```bash
$ sudo ./add_server
```

Run the client (terminal 2):
```bash
$ sudo ./add_client localhost 15 20
```