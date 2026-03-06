import java.rmi.Remote;
import java.rmi.RemoteException;

public interface CatService extends Remote {
    boolean openFile(String filename) throws RemoteException;
    String nextLine() throws RemoteException;
    boolean closeFile() throws RemoteException;
}
