import java.time.Instant;
import java.text.*; 
import java.util.*;
import java.io.*;
import java.lang.Math;
public class java_world{
    public static final int LENGTH = 36;
    public static String secret = "";
    public static String input = "";
    public static long key = 0;
    public static String gen(Collator coll){
        try {
            File pass = new File("password.txt");
            Scanner scan = new Scanner(pass);
            int c = 0;
            while(scan.hasNext()&&c<LENGTH){
                secret += scan.next();
                c++;
            }
            scan.close();
        }
        catch(FileNotFoundException e){
            System.out.println("Something is missing .. ");
            System.exit(1);
        }
        Random rand = new Random();
        Instant now = Instant.now();
        long seed = now.getEpochSecond();
        rand.setSeed(seed);
        int i;
        String longkey = "";
        for(i=0;i<(36+seed%10);i++){
            longkey += (char)(97+rand.nextInt(25));
        }
        coll.setStrength((int)seed%2 + 2);
        return longkey;
    }
    public static int trash(int x){
        int i;
        String xx = Integer.toBinaryString(x),res="";
        for(i=0;i<xx.length();i++){
            res += xx.charAt(i) == '0' ? '1' : '0';
        }
        return Integer.parseInt(res, 2);
    }
    public static int[][] hide(String longkey){
        int i,j,x;
        String res="";
        int [] tab = new int[LENGTH];
        int [][] hidden = new int[9][8];
        for(i=(LENGTH/2 -1);i>=0;i--){
            tab[i] = (int)secret.charAt(i) ^ (160 >> (2 & 10));
        }   
        for(i=(LENGTH/2);i<LENGTH;i++){
            x = (int)secret.charAt(i);
            tab[i] = (x | 4 ) & (~x | ((-110 >> 5) - 1));
        }

        for(j=0,i=(longkey.length()-1);j<LENGTH && i>=0;i--,j++){
            res += i % 4 != 0 ? (char)((int)longkey.charAt(i % 4)  + (int)tab[j] - 100): (char)(((int)tab[j] ^ (int)longkey.charAt(j % 5) ));
            res += j % 2 == 0 ? longkey.charAt(j % 5) : longkey.charAt(i % 4);
        }
        int k = 0;
        for(i=0;i<9;i++){
            for(j=0;j<8;j++){
                hidden[i][j] = (int)res.charAt(k++);
            } 
        }
        hidden[8][7] += longkey.length();
        return hidden;
    }
    public static void read_input(){
        Scanner scan = new Scanner(System.in);
        System.out.println("-!- Welcome to the world of JAVA -!-");
        System.out.println("-!- Answer my questions first and I will tell u the flag later -!-");
        
        try {
            System.out.println("-?- What's your favorite number ? -?-");
            System.out.print(">>");
            key = scan.nextInt();
            System.out.println("-?- Can you tell me the secret to get the flag ? -?-");
            System.out.print(">>");
            scan.nextLine();
            input = scan.nextLine();
            scan.close();
        }
        catch(Exception e){
            System.out.println("/!\\ Something is wrong, try later please /!\\");
            System.exit(1);
        }
    }

    public static void print_flag(){
        try{
            File flagFile = new File("flag.txt");
            Scanner scan = new Scanner(flagFile);
            System.out.println(scan.nextLine());
            scan.close();
        }
        catch(FileNotFoundException e){
            System.out.println("flag file is missing !");
            System.exit(1);
        }
    }
    public static void main(String [] args){
        String longkey;
        int [][] hidden = new int [9][8];
        Collator myCollator = Collator.getInstance(Locale.US);
        longkey = gen(myCollator);
        hidden = hide(longkey);
        for(int i=0;i<9;i++){
            for(int k=0;k<8;k++){
                System.out.print(hidden[i][k]+" ");
            }
            System.out.println();
        }
        read_input();
        long x = 0;
        for(int i=0;i<36;i++){
            x += key + (int)secret.charAt(i);
        }
        x = x / 10;
        x = (long)Math.pow(x, 2);
        if((x - 665330436) == 0){
            myCollator.setStrength((int)Math.abs(x - key)%4);
        }
        if((myCollator.compare(secret , input.toUpperCase()))==0){
            print_flag();
        }
        else {
            System.out.println("maybe another time ..");
        }

    }
}