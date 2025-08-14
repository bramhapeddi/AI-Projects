package com.acme-banking-qa.api.base;

import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.builder.ResponseSpecBuilder;
import io.restassured.specification.RequestSpecification;
import io.restassured.specification.ResponseSpecification;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;

import static io.restassured.RestAssured.given;

public abstract class ApiTest {
    
    protected static RequestSpecification requestSpec;
    protected static ResponseSpecification responseSpec;
    
    @BeforeAll
    static void setup() {
        String baseUrl = System.getenv().getOrDefault("BASE_URL", "https://api.example.com");
        RestAssured.baseURI = baseUrl;
        
        // Common request specification
        requestSpec = new RequestSpecBuilder()
            .addHeader("Content-Type", "application/json")
            .addHeader("Accept", "application/json")
            .addHeader("User-Agent", "acme-banking-qa-API-Tests/1.0")
            .build();
        
        // Common response specification
        responseSpec = new ResponseSpecBuilder()
            .expectStatusCode(200)
            .expectContentType("application/json")
            .build();
    }
    
    @BeforeEach
    void setUp() {
        // Reset to default state before each test
        RestAssured.reset();
    }
    
    protected RequestSpecification given() {
        return RestAssured.given().spec(requestSpec);
    }
    
    protected String getAuthToken() {
        // Implement authentication logic here
        // This is a placeholder - implement based on your auth strategy
        return System.getenv().getOrDefault("API_TOKEN", "");
    }
    
    protected void setAuthHeader() {
        String token = getAuthToken();
        if (token != null && !token.isEmpty()) {
            requestSpec.header("Authorization", "Bearer " + token);
        }
    }
}