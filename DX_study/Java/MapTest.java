import java.util.LinkedHashMap;
import java.util.Map;

public class MapTest {
    public static void main(String[] args) {

        Map<String, Integer> scores = new LinkedHashMap<>();
		    
		    //put : map에 key:value를 추가한다. 
        scores.put("민수", 80);
        scores.put("지수", 90);
        scores.put("서준", 70);
			
				//entrySet() : 키만 목록화한다. 
        for (Map.Entry<String, Integer> entry : scores.entrySet()) {
            System.out.println(
                    entry.getKey() + " : " + entry.getValue()
            );
        }

        scores.put("태우", 100);
				
				//map의 내용들을 조회한다. 
        System.out.println(scores);
    }
}