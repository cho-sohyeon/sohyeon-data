package com.example.membercrud.service;

import com.example.membercrud.domain.Member;
import com.example.membercrud.exception.MemberNotFoundException;
import com.example.membercrud.mapper.MemberMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service // 이 클래스는 핵심 로직을 담당하는 서비스 클래스입니다. 알려주는 용도 
        // 이 어노테이션이 있으면 spring boot가 해당 클래스의 객체를 만들어서 
        // Bean으로 관리해줍니다. 
@Transactional(readOnly = true)
public class MemberService {

    private final MemberMapper memberMapper;

    // 생성자 주입: MemberService 객체를 만들려면 MemberMapper 객체가 필요합니다.
    public MemberService(MemberMapper memberMapper) {
        this.memberMapper = memberMapper;
    }

    public List<Member> findAll() {
        return memberMapper.findAll();
    }

    public Member findById(Long memberId) {
        return memberMapper.findById(memberId)
                .orElseThrow(() -> new MemberNotFoundException(memberId));
    }

    @Transactional
    public Member create(Member member) {
        member.setMemberId(null);
        member.setCreatedAt(null);
        memberMapper.insert(member);
        return findById(member.getMemberId());
    }

    @Transactional
    public Member update(Long memberId, Member member) {
        findById(memberId);
        member.setMemberId(memberId);
        member.setCreatedAt(null);
        memberMapper.update(member);
        return findById(memberId);
    }

    @Transactional
    public void delete(Long memberId) {
        if (memberMapper.deleteById(memberId) == 0) {
            throw new MemberNotFoundException(memberId);
        }
    }
}

