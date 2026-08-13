package com.example.membercrud.service;

import com.example.membercrud.exception.ApiExceptionHandler;
import com.example.membercrud.mapper.PostMapper;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.membercrud.domain.Post;

//이 클래스는 핵심 로직을 담고 싶은 서비스 클래스입니다. 의미
//내부에 @Component가 있으니 시작할 때 new PostService() 객체를 만들어줌 
//스프링부트 만드는 객체를 "빈(Bean)"
//스프링부트가 알아서 객체를 만들고 관리하니까 "제어의역전"
//                                내가 관리 안함, 스프링 부트가 함 
@Service
public class PostService {

    @Autowired 
    public PostMapper postMapper; 
    
    //게시물을 등록하는 메서드 
    //PostController에서 create 라는 메서드가 호출할 예정 
    private final ApiExceptionHandler apiExceptionHandler;

    PostService(ApiExceptionHandler apiExceptionHandler) {
        this.apiExceptionHandler = apiExceptionHandler;
    }

    public void insertPost(Post post) {
        System.out.println("게시물을 등록합니다");
        System.out.println("=== 입력받은 값 ===");
        System.out.println("제목: " + post.getTitle());
        System.out.println("내용: " + post.getContent());
        System.out.println("작성자 ID: " + post.getWriterId());
        System.out.println("작성 일시: " + post.getCreatedAt());
        System.out.println("패스워드: " + post.getPassword());

        validatePassword(post.getPassword());

        System.out.println("검증 완료! , DB에 적재합니다."); 
        postMapper.insertPost(post); 
    }

    //입력받은 패스워드 검증한다. 
    public void validatePassword(String inputPassword) {

    // 패스워드는 필수 입력이고 8자리 이상이어야 한다
        if (inputPassword == null || inputPassword.length() < 8) {
            throw new RuntimeException("패스워드는 필수 입력이며, 8자리 이상이어야 합니다.");
        } 

        // 패스워드는 빈 값이면 안된다.
        // trim() : 입력받은 문자열의 양쪽 공백을 제거한다.
        // 예) inputPassword가 "  pass1234   " 이런식일때 
        // inputPassword.trim() 의 결과로 "pass1234"를 반환한다. 
        // isEmpty()는 문자열이 공백("")인지 확인해서 
        // 공백이라면 true를 반환
        if (inputPassword.trim().isEmpty()) {
            throw new RuntimeException("패스워드는 필수 입력입니다.");        
        }

        // 패스워드는 숫자로만 이루어져야 한다.
        // 정규표현식 (db , python , java -> 고급표현식)
        // matches("\\d+") 숫자값이 매칭이 되는가? 
        // \\d 가 숫자 하나 , +기호가 1개 이상   \\d+ 숫자가 여러개라는 매칭?
        // 만약 "1234F5" 이런식이면 matches는 false를 반환 
        
    // if(inputPassword.matches("\\d+") == false) {..}
        // 조건식에 !를 붙이면 부정을 의미 , true -> false , false -> true
        if (!inputPassword.matches("\\d+")) {
            throw new RuntimeException("패스워드는 숫자로만 이루어져야 합니다.");
        }

        //패스워드는 20자리 이하여야 한다. 
        if (inputPassword.length() > 20) {
            throw new RuntimeException("패스워드는 20자리 이하이어야 합니다.");
        }
    }

    //게시글 한 건을 조회한다. 
    public Post selectPostById(Long postId) { 

        System.out.println("조회할 게시글 ID: " + postId); 
        Post post = postMapper.selectPostById(postId); 

        if(post == null) { 
            throw new RuntimeException("게시글을 못찾겠어요."); 
        }

        return post; 
    } 

    //게시글을 전체 조회한다.
    public List<Post> selectPostList() {
        
        System.out.println("전체 게시글 조회입니다."); 
        
        /* 
            List<Post> posts = postMapper.selectPostList)(); 
            return posts;
            처럼 해도 되는데 
            
            바로 리턴할거면 아래와 같이 써도 됨
        */

        return postMapper.selectPostList();
    }

    //사용자가 총 2개의 값
    //하나는 "나 이 게시물 수정하고 싶어요 -> 게시글ID"
    //@PathVariable

    //또 하나는 "이렇게 수정할거에요" -> 게시글내용 
    //@RequestBody 받게 될 것 

    //REST API 규칙 상, 특정 대상은 
    //      /api/posts/123 -> 123 게시물에 대한! 

    //게시글 한건을 조회한다. 
    //그리고 수정한 결과물을 반환해준다. 
    public Post updatePost(Long postId, Post post) {

        //@PathVaiable로 받았던 그 게시글ID 를 
        //body로 받았던 Post객체에 직접 추가 
        post.setPostId(postId); 
        int result = postMapper.updatePost(post); 

        //제대로 update 안된 상황
        if(result == 0) { 
            throw new RuntimeException("패스워드가 일치하지 않습니다."); 
        }

        //result가 0이 아니라는 이야기 
        //update된 후에 해당 게시글을 다시 반환해주기로 했음 
        
        Post updatedPost = postMapper.selectPostById(postId); 
        return updatedPost;

    }

    public void deletePost(Long postId, String password) {

        int result = postMapper.deletePost(postId, password) ; 

        if(result ==0) {
            throw new RuntimeException("삭제에 실패했습니다."); 
        }
    }
}