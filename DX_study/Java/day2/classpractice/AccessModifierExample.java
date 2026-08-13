package day2.classpractice;


class User {
    private String memberId;
    private String name;

    public User(String memberId,String name) {
        this.memberId=memberId;
        this.name=name;
    }

    public String getMemberId() {
        return memberId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name=name;
    }
}

public class AccessModifierExample {

    public static void main(String[]args) {
        
       //파라미터 2개를 입력받는 생성자를 이용해 객체 생성과 동시에 필드를 초기화한다. 
       User user=new User("member01","강태우");
        
       //getMemberId() 메서드로 데이터를 가져온다 (직접 필드 접근 금지!) 
       System.out.println(user.getMemberId());
       System.out.println(user.getName());

	   //setName(이름)으로 데이터를 수정한다 (직접 필드 접근 금지!) 
       user.setName("김태우"); 
       System.out.println(user.getName());
    }
}