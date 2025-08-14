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
@Feature("getTransfer")
public class GettransferTest extends ApiTest {
    
    @Test
    @DisplayName("Get transfer details")
    @Description("Test GET /transfers/{transferId} endpoint")
    @Story("getTransfer")
    void testGettransferTest() {
        given()
            .spec(requestSpec)
            .pathParam("transferId", "test_transferId")
        .when()
            .request("GET", "/transfers/{transferId}")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("getTransfer - Invalid Request")
    @Description("Test GET /transfers/{transferId} with invalid data")
    @Story("getTransfer - Negative")
    void testGettransferTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("GET", "/transfers/{transferId}")
        .then()
            .statusCode(400);
    }
    
    @Test
    @DisplayName("getTransfer - Response Structure")
    @Description("Verify response structure for GET /transfers/{transferId}")
    @Story("getTransfer - Validation")
    void testGettransferTestResponseStructure() {
        given()
            .spec(requestSpec)
        .when()
            .request("GET", "/transfers/{transferId}")
        .then()
            .statusCode(200)
            .body("$", notNullValue());
    }
}