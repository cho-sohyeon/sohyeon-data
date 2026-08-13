package day2.classpractice;

//Student라는 틀(클래스) 만듬!
public class Student {

    //Student가 가지는 필드(속성)
    //String 문자열을 저장하는 자료형
    String studentId; 
    String name; 

    //int는 정수를 저장하는 자료형
    int age; 

    //public : 어디서든 이 메서드를 쓸 수 있음 
    //void : 반환값이 없음
    //sayHi : 함수이름 
    // ()   : 입력파라미터를 작성하는 구간 
    public void sayHi() {
        System.out.println(this.name + "이 인사합니다.");
    }

    /*
    //파이썬은 입력값이나 반환값에 자료형이 없다. 
    //자바는 입력값과 반환값 모두 자료형을 지정해야 한다. 
    //반환값이 없으면 void 로 표현 
    def sayHi() :
        print(name + "이 인사합니다")
    */

    // 2개의 정수를 입력받아서 합계를 반환하는 메서드 
    /*
    def plus(a,b) :
        return a+b 
    
    //자바 
    public int plus(int a, int b) {
        return a+b ; 
    }
        
    */

}