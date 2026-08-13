package com.example.membercrud.service;

import com.example.membercrud.domain.Member;
import com.example.membercrud.exception.MemberNotFoundException;
import com.example.membercrud.mapper.MemberMapper;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

class MemberServiceTest {

    private final MemberMapper memberMapper = mock(MemberMapper.class);
    private final MemberService memberService = new MemberService(memberMapper);

    @Test
    void findByIdReturnsMember() {
        Member member = new Member(1L, "kim@example.com", "김학생", null, LocalDateTime.now());
        when(memberMapper.findById(1L)).thenReturn(Optional.of(member));

        Member result = memberService.findById(1L);

        assertEquals("김학생", result.getName());
    }

    @Test
    void findByIdThrowsWhenMemberDoesNotExist() {
        when(memberMapper.findById(99L)).thenReturn(Optional.empty());

        assertThrows(MemberNotFoundException.class, () -> memberService.findById(99L));
    }

    @Test
    void deleteCallsMapper() {
        when(memberMapper.deleteById(1L)).thenReturn(1);

        memberService.delete(1L);

        verify(memberMapper).deleteById(1L);
    }
}

