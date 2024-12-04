import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize("username, password, expected_result", [
    ("demouser", "abc123", True),  # Credenciais válidas
])
def test_positive_login(page, username, password, expected_result):
    """Valida o login com diferentes combinações de credenciais."""
    # URL da aplicação
    base_url = "https://automation-sandbox-python-mpywqjbdza-uc.a.run.app"

    # Inicializa a página de login
    login_page = LoginPage(page)
    login_page.navigate_to(base_url)

    # Executa o login
    login_page.login(username, password)

    # Valida o resultado
    assert login_page.is_logged_in() == expected_result, f"Login test failed for {username}/{password}"