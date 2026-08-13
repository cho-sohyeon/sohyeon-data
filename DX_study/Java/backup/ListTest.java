package blackup;
import java.util.ArrayList; 
import java.util.List;

public class ListTest {
    public static void main(String[] args) {
        List<String> tasks = new ArrayList<>(); 

        tasks.add("Java 문법 학습"); 
        tasks.add("Git 실습"); 
        tasks.add("프로젝트 주제 찾기"); 

        for (String task : tasks) {
            System.out.println(task); 
        }
    }
}
