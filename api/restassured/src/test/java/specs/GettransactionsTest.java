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
@Feature("getTransactions")
public class GettransactionsTest extends ApiTest {
    
    @Test
    @DisplayName("Get transaction history")
    @Description("Test GET /transactions endpoint")
    @Story("getTransactions")
    void testGettransactionsTest() {
        given()
            .spec(requestSpec)
            .queryParam("accountId", "test_accountId")
            .queryParam("fromDate", "test_fromDate")
            .queryParam("toDate", "test_toDate")
            .queryParam("limit", "test_limit")
            .queryParam("offset", "test_offset")
        .when()
            .request("GET", "/transactions")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("getTransactions - Invalid Request")
    @Description("Test GET /transactions with invalid data")
    @Story("getTransactions - Negative")
    void testGettransactionsTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("GET", "/transactions")
        .then()
            .statusCode(400);
    }
    
    @Test
    @DisplayName("getTransactions - Response Structure")
    @Description("Verify response structure for GET /transactions")
    @Story("getTransactions - Validation")
    void testGettransactionsTestResponseStructure() {
        given()
            .spec(requestSpec)
        .when()
            .request("GET", "/transactions")
        .then()
            .statusCode(200)
            .body("$", notNullValue());
    }
}