# Distributed Computing (CS332) | Assignment 2
## **Introduction to Java and Sockets**

---

**Student Name :** *Naishadh Rana* <br>
**Roll. No :** U23CS014

---

---

## Task 2: First Java Program

### Problem Statement
Create a simple Java program with a `main` method that prints a message to the console.

### Concept Understanding
- Java requires a `public static void main(String[] args)` entry point.
- `System.out.println()` writes to standard output.
- File name must match the public class name (`DC_Lab1.java` for `public class DC_Lab1`).
- Compile with `javac`, run with `java ClassName`.

### Code Explanation
- `public class DC_Lab1` — declares the main class.
- `main` method — JVM starts execution here.
- `System.out.println("Hello, Eclipse!")` — prints the string and a newline.

### Viva Prep
- **Q: Why does the filename have to match the class name?**  
  A: Java requires the public class name to match the filename for the compiler to locate it.
- **Q: What does `public static void main` mean?**  
  A: `public` = accessible from anywhere; `static` = no object needed; `void` = returns nothing; `main` = entry point; `String[] args` = command-line arguments.
- **Q: Difference between `print` and `println`?**  
  A: `println` adds a newline at the end; `print` does not.

---

## Task 3: Differences Between C++/Python and Java

### Problem Statement
Identify key differences in memory management, pointers, JVM role, program structure, and build/run process.

### Concept Understanding

| Aspect | Java | C++ | Python |
|--------|------|-----|--------|
| Memory | Automatic garbage collection | Manual (`new`/`delete`) | Reference counting + GC |
| Pointers | No pointer arithmetic; only references | Full pointer support | No explicit pointers |
| Execution | JVM interprets/JIT compiles bytecode | Compiled to native code | Interpreted (CPython VM) |
| Structure | One public class per file; packages | Headers + source files | Modules/scripts |
| Type Safety | Strongly typed, checked at compile | Strongly typed but less safe | Dynamically typed |

### Viva Prep
- **Q: Why doesn't Java have pointers?**  
  A: To improve safety—no direct memory access, no pointer arithmetic, no dangling pointers.
- **Q: What is the JVM?**  
  A: Java Virtual Machine; it loads `.class` bytecode, verifies it, and executes via interpreter or JIT compiler.
- **Q: How is Java portable?**  
  A: Bytecode runs on any platform with a JVM ("write once, run anywhere").
- **Q: What does garbage collection do?**  
  A: Automatically reclaims memory from objects no longer reachable; programmer doesn't manually free memory.

---

## Task 4: Client–Server Model and Sockets

### Problem Statement
Understand what a socket is, the roles of client and server, and how TCP communication works.

### Concept Understanding
- **Socket**: An endpoint for two-way communication over a network (IP + port).
- **Server**: Binds to a port, listens for incoming connections, accepts them.
- **Client**: Initiates a connection to the server's IP and port.
- **TCP**: Reliable, ordered byte stream; uses 3-way handshake (SYN → SYN-ACK → ACK).

### Flow
1. Server creates `ServerSocket` on a port and calls `accept()` (blocks until client connects).
2. Client creates `Socket` to server's host:port.
3. Both get input/output streams; data flows bidirectionally.
4. Either side closes the socket to end communication.

### Viva Prep
- **Q: What is a port?**  
  A: A 16-bit number (0–65535) identifying a specific process on a host.
- **Q: Difference between TCP and UDP?**  
  A: TCP is reliable/ordered; UDP is faster but unreliable/unordered.
- **Q: What does `accept()` return?**  
  A: A new `Socket` representing the connection to the specific client.
- **Q: Can multiple clients connect to the same server port?**  
  A: Yes; server spawns a new socket per client while still listening on the original port.

---

## Task 5: Java Socket Classes

### Problem Statement
Study the purpose of `ServerSocket` and `Socket` classes and how messages are exchanged.

### Concept Understanding
- **`ServerSocket(int port)`**: Binds to a port and listens for connections.
- **`accept()`**: Blocks until a client connects; returns a connected `Socket`.
- **`Socket(String host, int port)`**: Client-side; initiates connection to server.
- **`getInputStream()` / `getOutputStream()`**: Returns streams for reading/writing data.

### Message Exchange
1. Client connects → both sides have streams.
2. Client writes to output stream → Server reads from input stream.
3. Server writes reply → Client reads.
4. Close sockets when done.

### Viva Prep
- **Q: Why wrap streams in `BufferedReader`/`PrintWriter`?**  
  A: For convenient line-based I/O (`readLine()`, `println()`); buffering improves efficiency.
- **Q: What does `PrintWriter(out, true)` mean?**  
  A: The `true` enables auto-flush on `println()`, ensuring data is sent immediately.
- **Q: What happens if client connects before server is listening?**  
  A: `Connection refused` exception on the client side.

---

## Task 6: Simple Echo Server/Client

### Problem Statement
Write a server that accepts a client connection, receives a message, and echoes it back.

### Concept Understanding
- Echo server = simplest request-response pattern.
- Demonstrates socket lifecycle: create → accept → read → write → close.
- Uses try-with-resources to auto-close sockets/streams.

### Code Explanation

**EchoServer.java**
- `ServerSocket(12345)` — listens on port 12345.
- `accept()` — waits for client; returns connected socket.
- `BufferedReader` wraps input stream for `readLine()`.
- `PrintWriter` wraps output stream for `println()`.
- Reads one line, prints it locally, echoes it back.

**EchoClient.java**
- `Socket("localhost", 12345)` — connects to server.
- Sends `"Hello from client"` via `println()`.
- Reads server's reply with `readLine()` and prints it.

### Output
```
# Server terminal
Echo server listening on port 12345
Received: Hello from client

# Client terminal
Server replied: Hello from client
```

### Viva Prep
- **Q: Why use try-with-resources?**  
  A: Automatically closes resources (sockets, streams) even if exceptions occur; prevents resource leaks.
- **Q: What if the server doesn't call `accept()`?**  
  A: Client's connection attempt times out or is refused.
- **Q: Can this server handle multiple clients?**  
  A: No; it accepts one client, echoes one message, then exits. For multi-client, use threads or a loop.
- **Q: What does `out.println(line)` do on the server?**  
  A: Sends the same message back to the client (echo).
- **Q: How would you make the server persistent?**  
  A: Wrap `accept()` in a `while(true)` loop and spawn a thread per client.

---

## Key Takeaways
1. Java's `main` method is the entry point; class name must match filename.
2. Java uses GC and references instead of manual memory/pointers for safety.
3. JVM provides portability and runtime services (GC, security, class loading).
4. Sockets are endpoints; `ServerSocket` listens, `Socket` connects.
5. TCP ensures reliable, ordered delivery; UDP is faster but unreliable.
6. Echo server demonstrates the basic socket lifecycle: listen → accept → read → write → close.
