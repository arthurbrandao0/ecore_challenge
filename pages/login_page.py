from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator('input[name="username"]')
        self.password_input = page.locator('input[name="password"]')
        self.login_button = page.locator('#btnLogin')

    def navigate_to(self, url: str):
        """Navega até a URL especificada."""
        self.page.goto(url)

    def login(self, username: str, password: str):
        """Preenche os campos de login e clica no botão."""
        self.email_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def is_logged_in(self) -> bool:
        """Verifica se o login foi bem-sucedido."""
        return self.page.url.endswith("account")  # Ajuste a URL de verificação se necessário
