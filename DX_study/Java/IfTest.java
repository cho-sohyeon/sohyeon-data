public class IfTest {
    public static void main(String[] args) {

        int score = 75;
        String subject = "수학";

        if (score >= 60) {
            System.out.println("합격");
        } else {
            System.out.println("불합격");
        }

        if (score >= 60 && subject.equals("수학")) {
            System.out.println("수학 과목 60점 이상입니다");
        } else {
            System.out.println("수학 과목이 아니거나 60점 미만입니다.");
        }

    }
}