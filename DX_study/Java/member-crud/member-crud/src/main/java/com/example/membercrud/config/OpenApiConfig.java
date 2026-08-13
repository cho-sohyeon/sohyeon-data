package com.example.membercrud.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "회원 CRUD 실습 API",
                version = "1.0",
                description = "Spring Boot, MyBatis, Oracle을 이용한 회원 CRUD 실습"
        )
)
public class OpenApiConfig {
}
