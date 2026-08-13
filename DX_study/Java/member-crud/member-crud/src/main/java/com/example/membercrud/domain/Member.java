package com.example.membercrud.domain;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.time.LocalDateTime;

/**
 * MEMBERS 테이블의 한 행(row)과 1:1로 대응하는 DTO/Domain 클래스입니다.
 */
public class Member {

    private Long memberId;          // MEMBER_ID NUMBER

    @NotBlank(message = "이메일은 필수입니다.")
    @Email(message = "이메일 형식이 올바르지 않습니다.")
    @Size(max = 100)
    private String email;           // EMAIL VARCHAR2(100)

    @NotBlank(message = "이름은 필수입니다.")
    @Size(max = 50)
    private String name;            // NAME VARCHAR2(50)

    @Size(max = 20)
    private String phone;           // PHONE VARCHAR2(20)

    private LocalDateTime createdAt; // CREATED_AT TIMESTAMP

    public Member() {
        // MyBatis와 JSON 변환기가 사용하는 기본 생성자
    }

    public Member(Long memberId, String email, String name, String phone, LocalDateTime createdAt) {
        this.memberId = memberId;
        this.email = email;
        this.name = name;
        this.phone = phone;
        this.createdAt = createdAt;
    }

    public Long getMemberId() { return memberId; }
    public void setMemberId(Long memberId) { this.memberId = memberId; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}

