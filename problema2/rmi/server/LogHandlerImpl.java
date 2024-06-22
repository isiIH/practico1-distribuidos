import java.rmi.RemoteException;
import java.nio.file.*;
import java.io.IOException;

public class LogHandlerImpl implements LogHandler {

    private static final String logFilename = "logServer.csv";

    @Override
    public boolean registerLog(String logContent) throws RemoteException {
        try{
            Files.write(Paths.get(logFilename), logContent.getBytes(), StandardOpenOption.APPEND);
        }
        catch (IOException e) {
            return false;
        }

        return true;
    }

}
