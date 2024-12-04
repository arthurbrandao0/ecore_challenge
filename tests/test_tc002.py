import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize("username, password", [
    ("Demouser", "abc123"),  # Caso inválido (Case Sensitive)
    ("demouser_", "xyz"),  # Usuário com underline
    ("demouser", "nananana"),  # Senha incorreta
    ("demouser", "abc123"),  # Teste duplicado proposital
])
def test_negative_login(page, username, password):
    """Valida que a aplicação exibe um alerta para credenciais inválidas."""
    # URL da aplicação
    base_url = "https://automation-sandbox-python-mpywqjbdza-uc.a.run.app"

    # Inicializa a página de login
    login_page = LoginPage(page)
    login_page.navigate_to(base_url)

    # Executa o login
    login_page.login(username, password)

    # Localiza o alerta de erro
    error_alert = page.locator('div.alert.alert-danger')
    assert error_alert.is_visible(), "Error alert is not visible with invalid credentials."

    # Valida o texto do alerta
    alert_text = error_alert.text_content().strip()
    assert alert_text == "Wrong username or password.", f"Unexpected alert text: {alert_text}"
