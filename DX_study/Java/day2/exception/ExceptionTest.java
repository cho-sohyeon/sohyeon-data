package day2.exception;

import java.util.InputMismatchException;
import java.util.Scanner;

public class ExceptionTest {
    public static void main(String[] args) { 

        Scanner sc = new Scanner(System.in);
        System.out.println("숫자를 입력하세요 : ");

        try { //이 사이의 코드에서 예외가 발생하면 잡겠다

            int number = sc.nextInt();
            System.out.println("작성한 숫자는 " + number + "입니다");

        } catch (InputMismatchException e) { //해당 예외를 처리하겠다.

            System.out.println("숫자를 입력해주세요.");

        } finally {
            System.out.println("이 곳은 예외가 터지든 아니든 실행되는 공간입니다.");
            sc.close();
        }
    }
}
