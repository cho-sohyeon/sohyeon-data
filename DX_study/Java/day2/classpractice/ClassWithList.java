package day2.classpractice;

import java.util.ArrayList;
import java.util.List;


//이 Member 코드를 더 줄이고 싶다면 나중에 어노테이션을 활용하면 됩니다.
class Member {
    private String memberId;
    private String password;
    private String name;

    public Member(String memberId, String password, String name) {
        this.memberId = memberId;
        this.password = password;
        this.name = name;
    }

    public String getMemberId() {
        return memberId;
    }

    public String getPassword() {
        return password;
    }

    public String getName() {
        return name;
    }
}

public class ClassWithList {
    public static void main(String[] args) {
				
		//중요! 타입을 Member 클래스라는 참조타입으로 받는다. 
        List<Member> members = new ArrayList<>();
				
		//객체를 생성하면서 List에 추가한다. 
        members.add(new Member("member01", "1234", "강태우"));
        members.add(new Member("member02", "5678", "김현철"));
        members.add(new Member("member03", "9999", "이수민"));

        // 전체 회원 출력
        for (Member member : members) {
            System.out.println(member.getMemberId() + ", " + member.getName());
        }

        // 특정 아이디 회원 찾기
        String targetId = "member02";
				
				
		//getMemberId() 는 memberId를 반환한다. (현재 String) 
        for (Member member : members) {
            if (member.getMemberId().equals(targetId)) {
                System.out.println("찾은 회원 : " + member.getName());
            }
        }
    }
}
