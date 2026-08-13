package day2.classpractice;

//계산기 클래스
//기능 : 더하기, 빼기, 곱하기, 나누기, 제곱하기
public class MyCalculator {

    /*속성*/
    //따로 관리할 속성이 없으므로 입력하지 않음

    /*기능*/
    //더하다
    int add(int firstNum, int secondNum) {
        System.out.println("입력받은 " + firstNum + " 와 " + secondNum + "를 더합니다.");
        return firstNum + secondNum ;
    }
    
    //빼다 
    int minus(int firstNum , int secondNum ) {
        System.out.println("입력받은 " + firstNum + " 에서 " + secondNum +"를 뺍니다.");
        return firstNum - secondNum; 
    }
} 