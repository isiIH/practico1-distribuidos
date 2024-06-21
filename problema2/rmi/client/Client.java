import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.File;  
import java.io.FileNotFoundException;  
import java.util.Scanner; 

public class Client {

    private static final int PORT = 4000;
    public static void main(String [] args){
        String filename, logContent;

        if (args.length != 1) {
            System.err.printf("Debe ingresar nombre del archivo log");
            return;
        }

        try{
            filename = args[0];

            File myObj = new File(filename);
            Scanner myReader = new Scanner(myObj);

            logContent = "";
            while (myReader.hasNextLine()) {
                logContent += myReader.nextLine() + "\n";
            }

            Registry registry = LocateRegistry.getRegistry("127.0.0.1", PORT);
            LogHandler logImpl = (LogHandler) registry.lookup("LogHandler");

            System.out.println(logImpl.registerLog(logContent));
        
        } catch(Exception e){
            System.err.println("Logger Excepcion:");
            e.printStackTrace();
            System.exit(1);
        }

    }
}
