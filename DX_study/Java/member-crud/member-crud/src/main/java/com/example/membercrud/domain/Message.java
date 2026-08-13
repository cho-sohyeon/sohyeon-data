package com.example.membercrud.domain;

public class Message {
    public String name; 
    public String message;
}


//@RequestBody Message message 
//@RequestBody의 역할: 사용자의 json데이터를 알아서 자바 클래스의 객체와 매핑해줌 
//                       json의 key와 자바 필드명이 동일해야 함 
//사용자의 입력값을 알아서 맞춰가지고 Message 클래스의 값과 매칭 

/*
{
    "name" : "강태우" , 
    "message" : "하이용"
}
*/