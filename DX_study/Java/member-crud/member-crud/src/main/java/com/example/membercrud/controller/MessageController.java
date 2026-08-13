package com.example.membercrud.controller;

import java.util.ArrayList;
import java.util.List; 

import org.springframework.web.bind.annotation.RestController;

import com.example.membercrud.domain.Message;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import io.swagger.v3.oas.annotations.tags.Tag;
 

@RestController // 이 클래스는 컨트롤러 역할을 합니다. 알림
                // REST API 용도 입니다.
                // 이 @RestController 안에 @Controller가 있고, 그 안에 @Conponent 가 있다. 
                // 프로그램을 실행하면 spring boot가 이 클래스에 대한 객체(bean)도 미리 만들어 놓습니다.


//swagger를 쓰고 있을떄, 해당 컨트롤러의 설명을 추가할 수 있음 
@Tag(name = "메시지 컨트롤러", description = "메세지를 주고받는 컨트롤러 입니다.")
public class MessageController {
    
    List<String> messages = new ArrayList<>(); // 필드 (메세지를 보낼때 그것들을 저장) 
    
    //메서드를 정의
    //@GetMapping은 사용자가 GET method로 요청할 때 매칭됩니다
    // @GetMapping("/show-message") 는 사용자가 GET 방식으로 /show-message URL로 요청을 한다는 의미입니다.
    @GetMapping("/show-message") 
    public List<String> showMessage() {
        return messages; 
    }

    //@PostMapping은 사용자가 POST Method로 요청할 때 매칭 (보통, 데이터를 등록하고 싶을 때 post를 쓴다)
    //@PostMapping("/send-message") 는 사용자가 POST 방식으로 send-message URL로 요청한다.
    @PostMapping("/send-message")
    public Message sendMessage( @RequestBody Message msg) {  //@RequestBody 어노테이션의 의미: 사용자가 {"message" : "안녕"} 처럼 보내면
    
        System.out.println("보낸 사람 : " + msg.name); 
        System.out.println("메세지 : " + msg.message  );
        messages.add(msg.name + "|" + msg.message   ); 
        return msg; 

}
}
