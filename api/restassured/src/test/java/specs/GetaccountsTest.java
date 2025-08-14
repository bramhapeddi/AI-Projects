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
@Feature("getAccounts")
public class GetaccountsTest extends ApiTest {
    
    @Test
    @DisplayName("Get user accounts")
    @Description("Test GET /accounts endpoint")
    @Story("getAccounts")
    void testGetaccountsTest() {
        given()
            .spec(requestSpec)
            .queryParam("type", "test_type")
            .queryParam("status", "test_status")
        .when()
            .request("GET", "/accounts")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("getAccounts - Invalid Request")
    @Description("Test GET /accounts with invalid data")
    @Story("getAccounts - Negative")
    void testGetaccountsTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("GET", "/accounts")
        .then()
            .statusCode(400);
    }
    
    @Test
    @DisplayName("getAccounts - Response Structure")
    @Description("Verify response structure for GET /accounts")
    @Story("getAccounts - Validation")
    void testGetaccountsTestResponseStructure() {
        given()
            .spec(requestSpec)
        .when()
            .request("GET", "/accounts")
        .then()
            .statusCode(200)
            .body("$", notNullValue());
    }
}