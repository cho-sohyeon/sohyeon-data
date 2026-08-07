import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class TodoList {

    public static void main(String[] args) { 

        //메뉴화면 -> 1 할일추가 2 할일제거 3 프로그램종료 
        int userPick = 0; 
        Scanner sc = new Scanner(System.in);
        List<String> todos = new ArrayList<>(); //todos = [] 의 java 버전 

        while(userPick != 3) { 

            System.out.println("숫자를 입력하세요"); 
            System.out.println("1. 할일추가 2.할일제거 3.프로그램종료"); 
            userPick = sc.nextInt(); //사용자 입력으로 숫자를 받는다. 

            if(userPick ==3) {
                System.out.println("프로그램 종료"); 
                break; 
            }

            if(userPick == 1) { 
                System.out.println("1번을 선택했습니다."); 
                System.out.println("할일을 입력하세요."); 
                
                sc.nextLine();
                String todo = sc.nextLine(); //문자열을 입력받는다. 
                todos.add(todo);
                System.out.println("todos => " + todos);  
            } else if(userPick ==2) {
                System.out.println("2번을 선택했습니다.");
                System.out.println("삭제할 할일을 입력하세요.");
                System.out.println("todos => " + todos); 
            }
        }
    }
}

