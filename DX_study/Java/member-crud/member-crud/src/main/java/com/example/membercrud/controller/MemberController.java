package com.example.membercrud.controller;

import com.example.membercrud.domain.Member;
import com.example.membercrud.service.MemberService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/api/members")
@CrossOrigin(origins = "http://localhost:5173")
@Tag(name = "회원 CRUD", description = "MEMBERS 테이블의 회원을 등록, 조회, 수정, 삭제합니다.")
public class MemberController {


    // 원래 의존성을 주입하는 방법이 여러개 

    // 그 중 첫번째 방법이 @Autowired 라는 어노테이션을 쓰는 것 
    // 의미: 스프링부트가 가지고 있는 bean, 연결해줘 ~ 

    /* 
    
    @Autowired
    private MemberService memberService; 
    
    */


    private final MemberService memberService;

    public MemberController(MemberService memberService) {
        this.memberService = memberService;
    }

    @GetMapping
    @Operation(summary = "전체 회원 조회")
    public List<Member> findAll() {
        return memberService.findAll();
    }

    @GetMapping("/{memberId}")
    @Operation(summary = "회원 한 명 조회")
    public Member findById(@PathVariable Long memberId) {
        return memberService.findById(memberId);
    }

    @PostMapping
    @Operation(summary = "회원 등록")
    public ResponseEntity<Member> create(@Valid @RequestBody Member member) {
        Member saved = memberService.create(member);
        return ResponseEntity.created(URI.create("/api/members/" + saved.getMemberId())).body(saved);
    }

    @PutMapping("/{memberId}")
    @Operation(summary = "회원 수정")
    public Member update(@PathVariable Long memberId, @Valid @RequestBody Member member) {
        return memberService.update(memberId, member);
    }

    @DeleteMapping("/{memberId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "회원 삭제")
    public void delete(@PathVariable Long memberId) {
        memberService.delete(memberId);
    }
}
