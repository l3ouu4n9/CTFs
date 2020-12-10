import java.io.Serializable;

public class AuthState implements Serializable {
    private static final long serialVersionUID = 123197894L;

    private boolean loggedIn = false;

    private String username = "Guest";

    public boolean isLoggedIn() {
        return true;
    }

    public void setLoggedInStatus(boolean paramBoolean) {
        this.loggedIn = paramBoolean;
    }
}