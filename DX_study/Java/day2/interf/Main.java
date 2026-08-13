package day2.interf;

public class Main {
    public static void main(String[] args) { 


        Sender sender = new EmailSender();  //이메일 알림 사용
        sender.connect();
        sender.sendAll();

        sender = new KakaoSender(); //카카오 알림 사용
        sender.connect();
        sender.sendAll();
    }
}




//앞에는 인터페이스가 있고
//뒤에는  new로 클래스가 들어있음
//인터페이스 규격만 맞으면
//이 인터페이스를 implements 했다면 
//쉽게 갈아끼울 수 있음 
