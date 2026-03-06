import java.io.*;
import java.net.*;
import java.util.*;

class P2PChat {
    static List<PrintWriter> peers = new ArrayList<>();
    static Set<String> connected = new HashSet<>();
    static int myPort;

    public static void main(String[] args) throws IOException {
        myPort = args.length > 0 ? Integer.parseInt(args[0]) : 7000;

        // listener thread
        new Thread(() -> {
            try (ServerSocket ss = new ServerSocket(myPort)) {
                System.out.println("Listening on " + myPort);
                while (true) add(ss.accept(), false);
            } catch (IOException e) { e.printStackTrace(); }
        }).start();

        // main input loop
        BufferedReader console = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("c host port | s msg | q");
        String line;
        while ((line = console.readLine()) != null) {
            if (line.startsWith("c ")) {
                String[] p = line.substring(2).split(" ");
                String host = p[0];
                int port = Integer.parseInt(p[1]);
                String key = host + ":" + port;
                if (!connected.contains(key)) {
                    add(new Socket(host, port), true);
                }
            } else if (line.startsWith("s ")) {
                String msg = line.substring(2);
                for (PrintWriter pw : peers) pw.println(msg);
            } else if (line.equals("q")) {
                System.exit(0);
            }
        }
    }

    static synchronized void add(Socket s, boolean initiator) throws IOException {
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));

        // exchange ports to identify peer
        out.println(myPort);
        int theirPort = Integer.parseInt(in.readLine());
        String host = s.getInetAddress().getHostAddress();
        String key = host + ":" + theirPort;

        // dedupe: only keep connection if we haven't connected yet
        if (connected.contains(key)) {
            s.close();
            return;
        }
        connected.add(key);
        peers.add(out);
        System.out.println("Connected: " + key);

        // reader thread
        new Thread(() -> {
            try {
                String m;
                while ((m = in.readLine()) != null) System.out.println("> " + m);
            } catch (IOException ignored) {}
        }).start();
    }
}
