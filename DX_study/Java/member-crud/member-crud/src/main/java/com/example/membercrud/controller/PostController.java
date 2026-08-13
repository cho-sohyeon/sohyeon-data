package com.example.membercrud.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.membercrud.domain.Post;
import com.example.membercrud.service.PostService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping("/api/posts")
@CrossOrigin(origins = "http://localhost:5173")
@Tag(
    name = "게시글 CRUD", 
    description = "게시글 등록, 조회, 수정, 삭제 API"
)
public class PostController {


    @Autowired
    private PostService postService; 


    //전체 게시글 조회 (GET 방식 / api/posts 요청) 
    @GetMapping
    @Operation(summary="전체 게시글 조회") 
    public List<Post> findAll() {

        /* 
            List<Post> posts = postService.selectPostList(); 
            return posts; 
        */
        
        return postService.selectPostList(); 
    }
    

    //게시글 한 건 조회 (GET 방식, /api/posts/123 ) 
    @GetMapping("/{postId}")
    @Operation(summary = "전체 게시글 한 건 조회") 
    public Post findById(@PathVariable("postId") Long postId) {
        
        Post post = postService.selectPostById(postId);

        return post;
    }

    //게시글 등록(자원 생성을 요청 POST 요청 + 데이터를 줄 때 요청바디) 
    // POST / api/posts 
    @PostMapping
    @Operation(summary = "게시글 등록") 
    //@Valid가 있으면 아 이 Post 에 대해서 유효성 검증을 하라는거구나 
    public Post create(@RequestBody @Valid Post post) {

        postService.insertPost(post); 

        return post; 
    }
    

    //게시글 수정 
    //PPUT / api/posts/123, 123번 게시물을 수정
    //수정할 데이터 body에 담아야 
    @PutMapping("/{postId}")
    @Operation(summary = "게시글 수정") 
    public Post update(@PathVariable("postId") Long postId
                    , @RequestBody @Valid Post post) {

        return postService.updatePost(postId, post); 
    }

    //게시글 삭제 
    //DELETE /api/posts/123? password=1234 
    @DeleteMapping("/{postId}")
    @Operation(summary = "게시글 삭제") 
    public String delete(@PathVariable("postId") Long postId
    , @RequestParam("password") String password ) {

        postService.deletePost(postId, password); 
        
        return "삭제되었습니다";
    }
}
