import java.io.*;
import java.net.*;
import java.util.*;

class BroadcastChatServer {
    private final List<PrintWriter> clients = Collections.synchronizedList(new ArrayList<>());

    public static void main(String[] args) throws IOException {
        new BroadcastChatServer().start();
    }

    private void start() throws IOException {
        try (ServerSocket server = new ServerSocket(6000)) {
            System.out.println("Broadcast server on 6000. Type exit from a client to leave.");
            while (true) {
                Socket socket = server.accept();
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                clients.add(out);
                new Thread(() -> handle(socket, out)).start();
            }
        }
    }

    private void handle(Socket socket, PrintWriter out) {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                if (line.equals("exit")) break;
                broadcast(line, out);
            }
        } catch (IOException ignored) {
        } finally {
            clients.remove(out);
            try { socket.close(); } catch (IOException ignored) {}
        }
    }

    private void broadcast(String message, PrintWriter sender) {
        synchronized (clients) {
            for (PrintWriter client : clients) {
                if (client != sender) {
                    client.println(message);
                }
            }
        }
    }
}
