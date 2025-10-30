import pytest

BASE_URL = "https://opensource-demo.orangehrmlive.com/"

def test_login_valid(page):
    """Test connexion valide"""
    page.goto(BASE_URL, timeout=60000)
    page.wait_for_selector('input[name="username"]', timeout=60000)
    page.fill('input[name="username"]', "Admin")
    page.fill('input[name="password"]', "admin123")
    page.click('button[type="submit"]')
    page.wait_for_selector('h6:has-text("Dashboard")', timeout=60000)
    assert page.is_visible('h6:has-text("Dashboard")')

def test_login_invalid(page):
    """Test connexion invalide"""
    page.goto(BASE_URL, timeout=60000)
    page.wait_for_selector('input[name="username"]', timeout=60000)
    page.fill('input[name="username"]', "Admin")
    page.fill('input[name="password"]', "wrongpass123")
    page.click('button[type="submit"]')
    page.wait_for_selector('p:has-text("Invalid credentials")', timeout=60000)
    assert page.is_visible('p:has-text("Invalid credentials")')

def test_logout(page):
    """Test déconnexion"""
    # Connexion
    page.goto(BASE_URL, timeout=60000)
    page.wait_for_selector('input[name="username"]', timeout=60000)
    page.fill('input[name="username"]', "Admin")
    page.fill('input[name="password"]', "admin123")
    page.click('button[type="submit"]')
    page.wait_for_selector('h6:has-text("Dashboard")', timeout=60000)

    # Ouvrir le menu utilisateur
    page.click('p.oxd-userdropdown-name')
    page.wait_for_selector('a:has-text("Logout")', state='visible', timeout=10000)

    # Cliquer sur logout
    page.locator('a:has-text("Logout")').click(timeout=20000)

    # Vérifier retour page login
    page.wait_for_selector('button[type="submit"]', timeout=60000)
    assert page.is_visible('button[type="submit"]')