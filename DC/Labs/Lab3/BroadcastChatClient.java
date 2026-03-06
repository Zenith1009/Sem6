import java.io.*;
import java.net.*;

class BroadcastChatClient {
    public static void main(String[] args) throws IOException {
        try (Socket socket = new Socket("localhost", 6000);
             BufferedReader serverIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter serverOut = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader console = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Connected. Type exit to quit.");

            Thread reader = new Thread(() -> {
                try {
                    String line;
                    while ((line = serverIn.readLine()) != null) {
                        System.out.println(line);
                    }
                } catch (IOException ignored) {
                }
            });
            reader.setDaemon(true);
            reader.start();

            while (true) {
                String msg = console.readLine();
                serverOut.println(msg);
                if (msg == null || msg.equals("exit")) break;
            }
        }
    }
}
