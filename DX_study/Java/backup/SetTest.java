package blackup;
import java.util.LinkedHashSet;
import java.util.Set;

public class SetTest {

    public static void main(String[] args) {

        Set<String> names = new LinkedHashSet<>();

        names.add("민수");
        names.add("지수");
        names.add("서준");

        for (String name : names) {
            System.out.println(name);
        }

        names.add("태우");
        names.add("민수");

        System.out.println(names);
    }
}