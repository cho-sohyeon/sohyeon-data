package day2.classpractice;

/* 사람의 정보를 표현하는 Person 클래스 */
class Person {

    /* 필드 */
    String name;    // 이름
    int age;        // 나이
    double weight;  // 몸무게
    double height;  // 키

    /* 생성자 */
    // 1. 기본 생성자 (아무런 생성자도 명시 되어 있지 않으면 자동으로 생성된다)
    public Person() {
    }

    // 2. 이름만 받는 생성자
    public Person(String name) {
        this.name=name;
    }

    // 3. 이름, 나이를 받는 생성자
    public Person(String name,int age) {
        this.name=name;
        this.age=age;
    }

	// 4. 모든 필드를 받는 생성자
    public Person(String name,int age,double weight,double height) {
        this.name=name;
        this.age=age;
        this.weight=weight;
        this.height=height;
    }
}

//파일 안에 class는 여러개일 수 있지만 
//public class는 단 하나! 이 이름이 파일명과 같아야 함
public class BasicClassWithConstructor {
    public static void main(String[]args) {

        // 기본 생성자 사용
        Person p1=new Person();
        System.out.println(p1.name); //아무것도 안나옴

        // 이름만 넣는 생성자 사용
        Person p2=new Person("태우");
        System.out.println(p2.name);

        // 이름, 나이를 함께 넣는 생성자 사용
        Person p3=new Person("현철",20);
        System.out.println(p3.name);
        System.out.println(p3.age);

        // 모든 필드를 넣는 생성자 사용
        Person p4=new Person("승희",25,50.3,170.5);
        System.out.println(p4.name);
        System.out.println(p4.age);
        System.out.println(p4.weight);
        System.out.println(p4.height);    
    }
}