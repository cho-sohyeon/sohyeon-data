package day2.interf;

//인터페이스는 구현을 하지 않는다. 
//무슨 기능을 구현하라는 명세(가이드)만 강제할 뿐이다. 
public interface Sender {

    //모든 사람에게 알림을 주는 기능 
    void sendAll() ; 
    
    //특정 대상이 특정 대상에게 알림을 주는 기능
    void send(String from , String to); 
    
    //통신을 위한 연결 코드
    void connect() ; 
} 

// 인터페이스: 이렇게 만들어야 메서드만 강제(실제 구현 X)
// 클래스 <- 이 인터페이스 "상속" <- 직접 구현 
// 클래스 입장에서는 
// 인터페이스가 요구한대로 만들 수 있기 때문에 제어가 가능 
