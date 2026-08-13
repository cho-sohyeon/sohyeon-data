package day2.classpractice;
public class Person {

     /* 필드 */
    String name;    // 이름
    int age;        // 나이
    double weight;  // 몸무게
    double height;  // 키

    // 메서드 없는 상태 

    // 생성자 추가
    public Person() {} // new Person() ; 

    public Person(String name, int age, double weight, double height) { // new Person("태우"); 
        this.name = name; 
        this.age = age ;
        this.weight = weight ; 
        this.height = height ; 
    }
}
