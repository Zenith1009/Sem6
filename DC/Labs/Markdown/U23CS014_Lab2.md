# Distributed Computing (CS332) | Assignment 2
## **Introduction to Java and Sockets**

---

**Student Name :** *Naishadh Rana* <br>
**Roll. No :** U23CS014

---

---

## Task 2: First Java Program

```java
public class DC_Lab1 {
    public static void main(String[] args) {
        System.out.println("Hello, Eclipse!");
    }
}
```

Output:
```bash
naish@MacBook-Air Lab2 % javac DC_Lab1.java 
naish@MacBook-Air Lab2 % java DC_Lab1 
Hello, Eclipse!
```

## Task 3: differences between C++ / Python and Java.

- Memory: Java has automatic garbage collection; no manual `delete`.
- Pointers: Only references; no pointer arithmetic; arrays are bounds-checked.
- JVM: Executes bytecode with JIT, GC, class loading, and security; makes Java portable.
- Structure: One public class per file; package names match folders; entry point is `public static void main(String[] args)`.
- Build/run: `javac` compiles to `.class` bytecode; `java` runs it on the JVM (C++ is AOT native; Python runs on CPython VM).

## Task 4: Client–Server Model
- Socket = two-way endpoint.
- Server: bind to host:port, listen, accept connections.
- Client: connect to server host:port.
- TCP: reliable byte stream; server handles each accepted connection with its own socket.

## Task 5: Java Socket Classes
- `ServerSocket`: listens on a port and `accept()` returns a connected `Socket`.
- `Socket`: represents the connected endpoint; read/write via streams.
- Message flow: client connects → streams available → client sends → server reads and can reply.

## Task 6: Simple client–server app using Java sockets.

Server waits for one client, echoes the received line back. <br>
Client sends a line and prints the reply.

**EchoServer.java**
```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class EchoServer {
    public static void main(String[] args) throws IOException {
        int port = 12345;
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Echo server listening on port " + port);
            try (Socket client = serverSocket.accept();
                 BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
                 PrintWriter out = new PrintWriter(client.getOutputStream(), true)) {

                String line = in.readLine();
                System.out.println("Received: " + line);
                out.println(line);
            }
        }
    }
}
```

**EchoClient.java**

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class EchoClient {
    public static void main(String[] args) throws IOException {
        String host = "localhost";
        int port = 12345;
        try (Socket socket = new Socket(host, port);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

            String message = "Hello from client";
            out.println(message);
            String reply = in.readLine();
            System.out.println("Server replied: " + reply);
        }
    }
}
```

Outputs (two terminals):
```bash
# Terminal A (Server)
naish@MacBook-Air Lab2 % java EchoServer 
Echo server listening on port 12345
Received: Hello from client
```
```bash
# Terminal B (Client)
naish@MacBook-Air Lab2 % java EchoClient 
Server replied: Hello from client
```
