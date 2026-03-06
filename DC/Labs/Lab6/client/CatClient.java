import java.rmi.Naming;

public class CatClient {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java CatClient <server-host> <filename>");
            return;
        }

        String host = args[0];
        String filename = args[1];

        try {
            CatService service = (CatService) Naming.lookup("rmi://" + host + ":1099/CatService");

            boolean opened = service.openFile(filename);
            if (!opened) {
                System.out.println("Failed to open file on server: " + filename);
                return;
            }

            System.out.println("Reading file from server: " + filename);
            String line;
            while ((line = service.nextLine()) != null) {
                System.out.println(line);
            }

            boolean closed = service.closeFile();
            System.out.println("File close status: " + closed);
        } catch (Exception e) {
            System.err.println("CatClient error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
