# User Stories for Acme Banking QA

## Story: User can login with valid credentials
**Labels:** @ui, @smoke, @functional
**Gherkin:**
```gherkin
Scenario: Successful login
  Given I am on the login page
  When I login as 'admin'/'password123'
  Then I should see the dashboard
  And I should see my account balance
```

## Story: User can transfer money between accounts
**Labels:** @ui, @functional, @regression
**Gherkin:**
```gherkin
Scenario: Money transfer between accounts
  Given I am logged in as 'user1'/'pass123'
  And I have sufficient balance in my checking account
  When I transfer $100 from checking to savings
  Then my checking balance should decrease by $100
  And my savings balance should increase by $100
  And I should see a confirmation message
```

## Story: API returns account information
**Labels:** @api, @smoke, @functional
**Gherkin:**
```gherkin
Scenario: Get account details
  Given I have a valid authentication token
  When I request account information for account '12345'
  Then I should receive a 200 status code
  And the response should contain account details
  And the account number should match '12345'
```

## Story: User cannot login with invalid credentials
**Labels:** @ui, @functional, @negative
**Gherkin:**
```gherkin
Scenario: Failed login with invalid password
  Given I am on the login page
  When I login as 'admin'/'wrongpassword'
  Then I should see an error message
  And I should remain on the login page
  And the error should indicate invalid credentials
```

## Story: Database connection health check
**Labels:** @backend, @smoke, @health
**Gherkin:**
```gherkin
Scenario: Database connectivity
  Given the application is running
  When I check the database health endpoint
  Then I should receive a 200 status code
  And the response should indicate database is healthy
  And the response time should be under 100ms
```

## Story: User can view transaction history
**Labels:** @ui, @functional, @regression
**Gherkin:**
```gherkin
Scenario: View transaction history
  Given I am logged in as 'user1'/'pass123'
  And I have previous transactions
  When I navigate to the transactions page
  Then I should see a list of my transactions
  And each transaction should show amount and date
  And the transactions should be sorted by date (newest first)
```

## Story: API validates request payload
**Labels:** @api, @functional, @negative
**Gherkin:**
```gherkin
Scenario: Invalid transfer request
  Given I have a valid authentication token
  When I send a transfer request with invalid amount
  Then I should receive a 400 status code
  And the response should contain validation errors
  And the error should specify which fields are invalid
```
