package day2.exception;

/*
     패스워드 검증기 클래스
     1. 패스워드는 8자리 이상
     2. 패스워드는 반드시 존재해야 함
     3. 12345678 패스워드는 쓸 수 없다.
 */
public class PasswordValidator {

    void isValidPassword(String password) throws RuntimeException {

        if(password.isEmpty()) {
            throw new RuntimeException("패스워드가 비어있습니다.");
        }

        if(password.length() < 8) {
            throw new RuntimeException("패스워드는 8자리 이상이어야 합니다.");
        }

        if(password.equals("12345678")) {
            throw new RuntimeException("12345678은 패스워드로 쓸 수 없습니다.");
        }
    }
}
