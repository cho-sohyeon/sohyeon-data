package com.example.membercrud.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import com.example.membercrud.domain.Post;

@Mapper // mybatis 가 사용할 클래스입니다.
        // 이 클래스는 나중에 SQL 이 들어있는 .xml 파일과 연결됩니다. 

public interface PostMapper {

    public void insertPost(Post post); //게시글 등록 

    public Post selectPostById(Long id);  //게시글 한건 조회

    public List<Post> selectPostList(); //게시글 전체 조회 

    //반환타입이 int인 이유? 
    //mybatis는 insert, update, delete 등의 작업을 하면 
    //처리한 행의 개수를 반환해준다.
    public int updatePost(Post post); //게시글 수정 


    //@Param 이라는 어노테이션 
    //입력파라미터가 2개 이상 일 때, 쿼리한테 헷갈리지 말라고
    //우리가 주려는 파라미터가 이거임! 이라고 명시해준다.
    //하나만 있으면 괜찮은데, 입력 파라미터가 둘 이상이라 명시하는 것 
    public int deletePost(@Param("postId") Long postId
                        , @Param("password") String password) ; 

}


/*
interface : 실제 구현된 코드는 아니고, 이런 메서드를 만드세요~ 규칙만 정해놓은 파일 

mybatis 가 알아서 이 인터페이스를 토대로 내부적으로 구현된 클래스를 만들어줍니다. 
*/