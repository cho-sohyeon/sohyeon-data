package day2.exception;

import java.util.InputMismatchException;
import java.util.Scanner;

public class TryCatchExample {
    public static void main(String[]args) {

        Scanner sc = new Scanner(System.in);
        System.out.println("10을 어떤 수로 나눌 건가요? 숫자를 입력해보세요.");

        try {

            int num = sc.nextInt();

            int result=10/num;
            System.out.println(result);

        } catch (ArithmeticException e) {
            System.out.println("0으로 나눌 수 없습니다.");
        } catch (InputMismatchException e2) {
            System.out.println("숫자를 입력하셔야 합니다.");
        }
    }
}