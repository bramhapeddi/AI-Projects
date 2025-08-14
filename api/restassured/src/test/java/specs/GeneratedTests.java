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
@Feature("Generated Tests")
public class GeneratedTests extends ApiTest {
    
    @Test
    @DisplayName("Health Check")
    @Description("Verify API health endpoint")
    @Story("API Health")
    void healthCheck() {
        given()
            .spec(requestSpec)
        .when()
            .get("/health")
        .then()
            .spec(responseSpec)
            .body("status", equalTo("UP"));
    }
    
    @Test
    @DisplayName("API Version")
    @Description("Verify API version endpoint")
    @Story("API Version")
    void apiVersion() {
        given()
            .spec(requestSpec)
        .when()
            .get("/version")
        .then()
            .spec(responseSpec)
            .body("version", notNullValue());
    }
    
    @ParameterizedTest
    @ValueSource(strings = {"users", "products", "orders"})
    @DisplayName("List Resources")
    @Description("Verify list endpoints return arrays")
    @Story("Resource Listing")
    void listResources(String resource) {
        given()
            .spec(requestSpec)
        .when()
            .get("/" + resource)
        .then()
            .spec(responseSpec)
            .body("$", hasKey("data"))
            .body("data", hasSize(greaterThanOrEqualTo(0)));
    }
}