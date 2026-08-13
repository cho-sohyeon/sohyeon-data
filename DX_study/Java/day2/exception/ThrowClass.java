package day2.exception;

import java.util.Scanner;

public class ThrowClass {

    public static void main(String[] args) { 

        Scanner sc = new Scanner(System.in);

        //미니 패스워드 검증기
        System.out.println("패스워드를 입력하세요(8자리 이상)");

        String password = sc.nextLine();
        if(password.length() < 8) {
            throw new RuntimeException("패스워드는 8자리 이상 입력하세요.");
        } else {
            System.out.println("패스워드 검증 성공");
        }
    }
}