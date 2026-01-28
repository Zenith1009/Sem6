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
