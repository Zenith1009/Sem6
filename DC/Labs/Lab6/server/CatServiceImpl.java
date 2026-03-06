import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class CatServiceImpl extends UnicastRemoteObject implements CatService {
    private BufferedReader reader;

    public CatServiceImpl() throws RemoteException {
        super(2001);
    }

    @Override
    public synchronized boolean openFile(String filename) throws RemoteException {
        closeFile();
        try {
            Path path = Path.of(filename);
            reader = Files.newBufferedReader(path);
            return true;
        } catch (IOException e) {
            reader = null;
            return false;
        }
    }

    @Override
    public synchronized String nextLine() throws RemoteException {
        if (reader == null) {
            return null;
        }
        try {
            return reader.readLine();
        } catch (IOException e) {
            return null;
        }
    }

    @Override
    public synchronized boolean closeFile() throws RemoteException {
        if (reader == null) {
            return false;
        }
        try {
            reader.close();
            reader = null;
            return true;
        } catch (IOException e) {
            reader = null;
            return false;
        }
    }
}
