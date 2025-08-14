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
@Feature("getHealth")
public class GethealthTest extends ApiTest {
    
    @Test
    @DisplayName("Health check endpoint")
    @Description("Test GET /health endpoint")
    @Story("getHealth")
    void testGethealthTest() {
        given()
            .spec(requestSpec)
        .when()
            .request("GET", "/health")
        .then()
            .statusCode(200)
            .contentType("application/json");
    }
    
    @Test
    @DisplayName("getHealth - Invalid Request")
    @Description("Test GET /health with invalid data")
    @Story("getHealth - Negative")
    void testGethealthTestInvalidRequest() {
        given()
            .spec(requestSpec)
            .body("invalid_data")
        .when()
            .request("GET", "/health")
        .then()
            .statusCode(400);
    }
    
    @Test
    @DisplayName("getHealth - Response Structure")
    @Description("Verify response structure for GET /health")
    @Story("getHealth - Validation")
    void testGethealthTestResponseStructure() {
        given()
            .spec(requestSpec)
        .when()
            .request("GET", "/health")
        .then()
            .statusCode(200)
            .body("$", notNullValue());
    }
}