package com.example.membercrud.domain;

import java.time.LocalDateTime;

import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Post {

    // 게시글 ID
    private Long postId;

    // 게시글 제목
    @Size(min= 1 , max = 200, message = "제목은 1자 이상 200자 이하로 입력해주세요.") 
    private String title;

    // 게시글 내용
    private String content;

    // 작성자 ID
    private Long writerId;

    // 작성 일시
    private LocalDateTime createdAt;

    //패스워드 
    private String password; 
}