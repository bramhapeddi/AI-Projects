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
@Feature("getAccountBalance")
public class GetaccountbalanceTest extends ApiTest {
    
    @Test
    @DisplayName("Get account balance")
    @Description("Test GET /accounts/{accountId}/balance endpoint")
    @Story("getAccountBalance")
    void testGetaccountbalanceTest() {
        given()
            .spec(requestSpec)
            .pathParam("accountId", "test_accountId")
        .when()
            .request("GET", "/accounts/{accountId}/balance")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("getAccountBalance - Invalid Request")
    @Description("Test GET /accounts/{accountId}/balance with invalid data")
    @Story("getAccountBalance - Negative")
    void testGetaccountbalanceTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("GET", "/accounts/{accountId}/balance")
        .then()
            .statusCode(400);
    }
    
    @Test
    @DisplayName("getAccountBalance - Response Structure")
    @Description("Verify response structure for GET /accounts/{accountId}/balance")
    @Story("getAccountBalance - Validation")
    void testGetaccountbalanceTestResponseStructure() {
        given()
            .spec(requestSpec)
        .when()
            .request("GET", "/accounts/{accountId}/balance")
        .then()
            .statusCode(200)
            .body("$", notNullValue());
    }
}