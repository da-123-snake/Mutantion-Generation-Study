import java.util.Scanner;

public class Main {
	
	public static void main(String[] args) {
		
		Scanner sc = new Scanner(System.in);
		int n = sc.nextInt();
		sc.close();
		
		if( n >= 42) {
			System.out.println("AGC0"+ (n+1));
		}else {
			System.out.println("AGC0"+ n);
		}
		
	}
}