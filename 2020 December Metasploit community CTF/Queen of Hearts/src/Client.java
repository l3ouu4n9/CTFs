import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;

public class Client {
    private Socket socket;

    private AuthState authState;

    private ObjectInputStream cliIn;

    private ObjectOutputStream cliOut;

    private BufferedReader userIn;

    public void printUsage() {
        System.out.println("Usage:\n\tjava -jar QOH_Client.jar <ip> <port>\n\n\twhere port is generally 9008");
    }

    public void cliLoop(String paramString, int paramInt) throws IOException, ClassNotFoundException {
        boolean bool = false;
        try {
            this.socket = new Socket(paramString, paramInt);
        } catch (UnknownHostException unknownHostException) {
            System.out.println("Failed to connect to host.");
            return;
        }
        this.cliIn = new ObjectInputStream(this.socket.getInputStream());
        this.cliOut = new ObjectOutputStream(this.socket.getOutputStream());
        this.userIn = new BufferedReader(new InputStreamReader(System.in));
        this.authState = (AuthState)this.cliIn.readObject();
        if (this.authState == null) {
            System.out.println("Could not receive the AuthState object");
            bool = true;
        }
        System.out.println("Successfully connected to the server!");
        while (!bool) {
            int i = -1;
            String str1 = "";
            str1 = this.cliIn.readUTF();
            System.out.println(str1);
            String str2 = this.userIn.readLine();
            try {
                i = Integer.parseInt(str2);
            } catch (NumberFormatException numberFormatException) {
                i = -1;
            }
            this.cliOut.writeInt(i);
            this.cliOut.flush();
            str1 = this.cliIn.readUTF();
            System.out.println(str1);
            if (str1.contains("invalid"))
                continue;
            switch (i) {
                case 1:
                    doList();
                case 2:
                    doDownload(this.userIn);
                case 3:
                    doAuthenticate(this.userIn);
            }
        }
    }

    public void doAuthenticate(BufferedReader paramBufferedReader) {
        String str = "";
        try {
            this.cliOut.writeObject(this.authState);
            str = this.cliIn.readUTF();
            System.out.println(str);
            if (str.contains("already authenticated"))
                return;
            String str1 = paramBufferedReader.readLine();
            this.cliOut.writeUTF(str1);
            this.cliOut.flush();
            str = this.cliIn.readUTF();
            System.out.println(str);
            this.authState = (AuthState)this.cliIn.readObject();
        } catch (IOException|ClassNotFoundException iOException) {
            System.out.println("Could not retrieve server's message regarding authentication");
            return;
        }
    }

    public void doList() {
        String str = "";
        try {
            str = this.cliIn.readUTF();
            System.out.println(str);
            str = this.cliIn.readUTF();
        } catch (IOException iOException) {
            System.out.println("Failed to receive a file listing from the server.");
            return;
        }
        System.out.println(str);
    }

    public void doDownload(BufferedReader paramBufferedReader) {
        String str = "";
        try {
            String str1;
            str = this.cliIn.readUTF();
            System.out.println(str);
            this.cliOut.writeObject(this.authState);
            str = this.cliIn.readUTF();
            System.out.println(str);
            if (str.contains("not authenticated"))
                return;
            do {
                str = this.cliIn.readUTF();
                System.out.println(str);
                str1 = paramBufferedReader.readLine();
                this.cliOut.writeUTF(str1);
                this.cliOut.flush();
                str = this.cliIn.readUTF();
                System.out.println(str);
            } while (!str.contains("Sending"));
            FileOutputStream fileOutputStream = new FileOutputStream(str1);
            int i = this.cliIn.readInt();
            System.out.println("File size received is " + i);
            byte[] arrayOfByte = new byte[i];
            this.cliIn.readFully(arrayOfByte, 0, i);
            fileOutputStream.write(arrayOfByte);
            fileOutputStream.close();
        } catch (IOException iOException) {
            System.out.println("Unable to download from the server");
        }
    }

    public static void main(String[] paramArrayOfString) throws IOException, ClassNotFoundException {
        Client client = new Client();
        if (paramArrayOfString.length != 2) {
            client.printUsage();
            return;
        }
        String str = paramArrayOfString[0];
        int i = Integer.parseInt(paramArrayOfString[1]);
        client.cliLoop(str, i);
        client.cliIn.close();
        client.cliOut.close();
        client.userIn.close();
    }
}
