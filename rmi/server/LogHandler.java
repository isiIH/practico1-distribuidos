import java.rmi.Remote; 
import java.rmi.RemoteException; 

public interface LogHandler extends Remote {

    public boolean registerLog(String logContent) throws RemoteException;
    
}
