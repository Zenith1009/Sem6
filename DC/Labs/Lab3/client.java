import java.io.*;
import java.net.*;

class Client {
    public static void main(String[] args) throws IOException {
        try (Socket socket = new Socket("localhost", 5001);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader console = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Connected. Type exit to quit.");
            while (true) {
                System.out.print("You> ");
                String msg = console.readLine();
                out.println(msg);
                if (msg == null || msg.equals("exit")) break;

                String reply = in.readLine();
                if (reply == null || reply.equals("exit")) break;
                System.out.println("Server> " + reply);
            }
        }
    }
}