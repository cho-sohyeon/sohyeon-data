package com.example.membercrud.mapper;

import com.example.membercrud.domain.Member;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.Optional;

@Mapper
public interface MemberMapper {
    List<Member> findAll();
    Optional<Member> findById(@Param("memberId") Long memberId);
    int insert(Member member);
    int update(Member member);
    int deleteById(@Param("memberId") Long memberId);
}

