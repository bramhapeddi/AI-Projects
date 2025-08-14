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
@Feature("logout")
public class LogoutTest extends ApiTest {
    
    @Test
    @DisplayName("User logout")
    @Description("Test POST /auth/logout endpoint")
    @Story("logout")
    void testLogoutTest() {
        given()
            .spec(requestSpec)
        .when()
            .request("POST", "/auth/logout")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("logout - Invalid Request")
    @Description("Test POST /auth/logout with invalid data")
    @Story("logout - Negative")
    void testLogoutTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("POST", "/auth/logout")
        .then()
            .statusCode(400);
    }
    
}