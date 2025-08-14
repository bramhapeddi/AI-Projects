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
@Feature("getAccount")
public class GetaccountTest extends ApiTest {
    
    @Test
    @DisplayName("Get account details")
    @Description("Test GET /accounts/{accountId} endpoint")
    @Story("getAccount")
    void testGetaccountTest() {
        given()
            .spec(requestSpec)
            .pathParam("accountId", "test_accountId")
        .when()
            .request("GET", "/accounts/{accountId}")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("getAccount - Invalid Request")
    @Description("Test GET /accounts/{accountId} with invalid data")
    @Story("getAccount - Negative")
    void testGetaccountTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("GET", "/accounts/{accountId}")
        .then()
            .statusCode(400);
    }
    
    @Test
    @DisplayName("getAccount - Response Structure")
    @Description("Verify response structure for GET /accounts/{accountId}")
    @Story("getAccount - Validation")
    void testGetaccountTestResponseStructure() {
        given()
            .spec(requestSpec)
        .when()
            .request("GET", "/accounts/{accountId}")
        .then()
            .statusCode(200)
            .body("$", notNullValue());
    }
}