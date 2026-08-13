package day2.interf;

public class EmailSender implements Sender{

    @Override
    public void sendAll() {
        System.out.println("모든 사용자에게 이메일을 보냅니다.");
    }

    @Override
    public void send(String from, String to) {
        System.out.println(from + "님이 " + to + "님에게 이메일 알림을 보냅니다.");
    }

    @Override
    public void connect() {
        System.out.println("이메일 서버에 접속합니다...");
    }
}