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
@Feature("createTransfer")
public class CreatetransferTest extends ApiTest {
    
    @Test
    @DisplayName("Create money transfer")
    @Description("Test POST /transfers endpoint")
    @Story("createTransfer")
    void testCreatetransferTest() {
        given()
            .spec(requestSpec)
            .body("{}") // TODO: Add proper request body based on schema
        .when()
            .request("POST", "/transfers")
        .then()
            .statusCode(201)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("createTransfer - Invalid Request")
    @Description("Test POST /transfers with invalid data")
    @Story("createTransfer - Negative")
    void testCreatetransferTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("POST", "/transfers")
        .then()
            .statusCode(400);
    }
    
}