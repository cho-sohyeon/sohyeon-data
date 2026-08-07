import java.util.HashMap;
import java.util.Map;

public class MapStructure {
    public static void main(String[] args) {

        /**
         * 1. Map 선언 및 초기화
           Map<K,V> 형태로 K :key , V:value 로 쌍으로 입력받습니다. 
           예) Map<String,String> 일 경우 
               {"NAME" : "강태우"} 등으로 저장
         */
        Map<String, String> userInfo = new HashMap<>();

        /**
         * 2. 데이터 추가
         * put(key, value)
         */
        userInfo.put("MEMBER_ID", "MEMBER01");
        userInfo.put("MEMBER_NAME", "강감찬");
        userInfo.put("AGE", "30");
        userInfo.put("PHONE", "01012345678");

        System.out.println(userInfo);

        /**
         * 3. 특정 데이터 조회
           key 값을 기반으로 value를 조회합니다. 
         * get(key)
         */
        String userAge = userInfo.get("AGE");
        System.out.println("나이 : " + userAge);

        /**
         * 4. 같은 key에 다시 put하면 값이 덮어써짐 (key중복이 안됨)
         */
        userInfo.put("MEMBER_NAME", "김혁수");
        System.out.println(userInfo);

        /**
         * 5. 특정 key 삭제
         */
        userInfo.remove("AGE");
        System.out.println(userInfo);

        /**
         * 6. 비어있는지 확인, 크기 확인
         */
        System.out.println("map 비었는지 확인 : " + userInfo.isEmpty());
        System.out.println("현재 map 사이즈 : " + userInfo.size());

        /**
         * 7. 특정 key 존재 여부 확인
         */
        System.out.println("MEMBER_ID 존재 여부 : " + userInfo.containsKey("MEMBER_ID"));
        System.out.println("EMAIL 존재 여부 : " + userInfo.containsKey("EMAIL"));

        /**
         * 8. 전체 비우기
         */
        userInfo.clear();
        System.out.println("clear 후 map : " + userInfo);
    }
} 
