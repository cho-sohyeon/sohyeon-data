package day2.classpractice;

public class Main {
    public static void main(String[] args) {
        
        //학생1 표현하기 
        Student student1 = new Student(); 
        Student student2 = new Student(); 

        student1.studentId = "S0001"; 
        student1.name = "강태우";
        student1.age = 30; 

        student2.studentId = "S0002"; 
        student2.name = "김현철";
        student2.age = 20; 

        student1.sayHi();
        student2.sayHi();

    }
}
