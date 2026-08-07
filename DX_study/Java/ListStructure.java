import java.util.ArrayList;
import java.util.List;

public class ListStructure {
    public static void main(String[] args) {

        /**
         * 1. List 선언 및 초기화
         * 꺽쇠(<>)의 의미 : 해당 타입으로 리스트를 사용하겠다는 의미입니다.   
         * 참고로 참조타입만 사용할 수 있으며 Integer는 int의 Wrapper클래스입니다. 
         * 해당 내용은 chapter5에서 다룹니다.        
         */
        List<String> names = new ArrayList<>();
        List<Integer> scores = new ArrayList<>();

        /**
         * 2. 데이터 추가
         *    리스트의 add 메서드로 타입에 맞는 요소를 추가합니다. 
         */
        names.add("강감찬");
        names.add("공유");

        scores.add(200);
        scores.add(400);
        scores.add(500);
        System.out.println(names);
        System.out.println(scores);

        /**
         * 3. 데이터 삭제
         * remove(index) : 해당 인덱스의 데이터를 삭제합니다. 
         * 혹은 remove(data) 처럼 특정 data를 명시해 삭제할 수 있습니다. 
         */
        scores.remove(1); // 400 삭제
        System.out.println(scores);

        /**
         * 4. 특정 위치 데이터 수정
         * set(index, value)
         */
        names.set(1, "낫공유");
        System.out.println(names);

        /**
         * 5. 특정 위치 데이터 조회
         * get(index)
         */
        System.out.println("0번째 이름 : " + names.get(0));

        /**
         * 6. 리스트 크기 확인
         */
        int namesSize = names.size();
        System.out.println("현재 등록된 이름 개수 : " + namesSize);

        /**
         * 7. 비우기
         */
        scores.clear();
        System.out.println(scores);
        System.out.println("현재 등록된 점수 개수 : " + scores.size());

        /**
         * 8. 비어있는지 확인-> 결과로 true/false반환
         */
        System.out.println("names 비었는지 여부 : " + names.isEmpty());
        System.out.println("scores 비었는지 여부 : " + scores.isEmpty());

        /**
         * 9. 특정 값 포함 여부 확인 -> 결과로 true/false 반환
         */
        System.out.println(names.contains("공유"));
        System.out.println(names.contains("강감찬"));
    }
}