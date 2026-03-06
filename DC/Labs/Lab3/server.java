import java.io.*;
import java.net.*;

class Server {
    public static void main(String[] args) throws IOException {
        try (ServerSocket server = new ServerSocket(5001);
             Socket socket = server.accept();
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader console = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Server ready on 5001. Type exit to quit.");
            while (true) {
                String fromClient = in.readLine();
                if (fromClient == null || fromClient.equals("exit")) break;
                System.out.println("Client: " + fromClient);

                System.out.print("Server> ");
                String reply = console.readLine();
                out.println(reply);
                if (reply == null || reply.equals("exit")) break;
            }
        }
    }
}