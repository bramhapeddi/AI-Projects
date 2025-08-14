package com.acme-banking-qa.api.specs;

import com.acme-banking-qa.api.base.ApiTest;
import io.qameta.allure.Description;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

@Epic("acme-banking-qa API")
@Feature("login")
public class LoginTest extends ApiTest {
    
    @Test
    @DisplayName("User login")
    @Description("Test POST /auth/login endpoint")
    @Story("login")
    void testLoginTest() {
        given()
            .spec(requestSpec)
            .body("{}") // TODO: Add proper request body based on schema
        .when()
            .request("POST", "/auth/login")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("login - Invalid Request")
    @Description("Test POST /auth/login with invalid data")
    @Story("login - Negative")
    void testLoginTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("POST", "/auth/login")
        .then()
            .statusCode(400);
    }
    
}