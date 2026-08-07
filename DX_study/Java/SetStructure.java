import java.util.HashSet;
import java.util.Set;

public class SetStructure {
    public static void main(String[] args) {

        /*
         * 1. Set 선언 및 초기화
         */
        Set<String> distinctMenu = new HashSet<>();

        /*
         * 2. 데이터 추가
         */
        distinctMenu.add("짬뽕");
        distinctMenu.add("볶음밥");
        distinctMenu.add("짬뽕"); // 중복 추가

        System.out.println(distinctMenu);

        /*
         * 3. 특정 값 포함 여부 확인
         */
        System.out.println(distinctMenu.contains("짬뽕"));
        System.out.println(distinctMenu.contains("자장면"));

        /*
         * 4. 특정 값 삭제
         */
        distinctMenu.remove("짬뽕");
        System.out.println(distinctMenu);

        /*
         * 5. 비었는지 확인, 크기 확인
         */
        System.out.println("set 비었는지 확인 : " + distinctMenu.isEmpty());
        System.out.println("현재 set 사이즈 : " + distinctMenu.size());

        /*
         * 6. 전체 비우기
         */
        distinctMenu.clear();
        System.out.println("clear 후 set : " + distinctMenu);
    }
}