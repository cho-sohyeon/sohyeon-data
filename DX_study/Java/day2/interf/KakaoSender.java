package day2.interf;

public class KakaoSender implements Sender{
    
    @Override 
    public void sendAll() { 
        System.out.println("카카오 알림을 보냅니다."); 
    }
    @Override 
    public void send(String from , String to){
        System.out.println(from +"이" + to + "에게 카카오 알림을 보냅니다."); 
    }
    @Override
    public void connect() {
        System.out.println("카카오 알림을 연결합니다."); 
    }

    //인터페이스에서 강제한 메서드를 모두 구현하니 
    //KakaoSender에 빨간 줄이 사라진 것을 볼 수 있음 

    //인터페이스가 왜 필요할까? 
    //규격을 미리 정해놓으면 다양한 클래스에 대해 정해진 규칙을 만들 수 있음 

    //예) 
    //DBConnector 인터페이스 (연결하기(), 접속하기(), 쿼리실행하기 ....)

    //OracleConnector구현체 
    //MysqlConnector구현체 
    //PostgreConnector구현체 
    //이미 인터페이스가 규격화되어 있으므로 쉽게 갈아끼울 수 있음 

    //인터페이스는 구현해야하는 메서드의 선언만 존재한다.
    //이거를 클래스가 implements(구현)을 해야 한다. 

}
