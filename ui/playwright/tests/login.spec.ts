import { test, expect } from '@playwright/test';
import { LoginPage } from '../src/pages/LoginPage';
import { DashboardPage } from '../src/pages/DashboardPage';

test.describe('Login Functionality', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
  });

  test('valid user can login successfully', async ({ page }) => {
    await loginPage.goto();
    await loginPage.expectLoginFormVisible();
    
    await loginPage.login(process.env.TEST_USERNAME || 'testuser', 
                         process.env.TEST_PASSWORD || 'password');
    
    await dashboardPage.expectDashboardLoaded();
    await dashboardPage.expectUserLoggedIn(process.env.TEST_USERNAME || 'testuser');
  });

  test('invalid credentials show error message', async ({ page }) => {
    await loginPage.goto();
    await loginPage.login('invalid', 'wrong');
    await loginPage.expectErrorMessage('Invalid credentials');
  });

  test('empty form submission shows validation errors', async ({ page }) => {
    await loginPage.goto();
    await loginPage.login('', '');
    await loginPage.expectErrorMessage('Username and password are required');
  });
});