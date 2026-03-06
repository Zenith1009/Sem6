import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class CatServer {
    public static void main(String[] args) {
        try {
            String rmiHostname = System.getenv("RMI_HOSTNAME");
            if (rmiHostname != null && !rmiHostname.isBlank()) {
                System.setProperty("java.rmi.server.hostname", rmiHostname);
                System.out.println("Using java.rmi.server.hostname=" + rmiHostname);
            }

            Registry registry = LocateRegistry.createRegistry(1099);
            CatService service = new CatServiceImpl();
            registry.rebind("CatService", service);
            System.out.println("CatServer ready on RMI registry port 1099 and object port 2001");
        } catch (Exception e) {
            System.err.println("CatServer error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
