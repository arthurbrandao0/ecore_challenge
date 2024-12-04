import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize("username, password, expected_details", [
    (
        "demouser", "abc123",
        {
            "HotelName": "Rendezvous Hotel",
            "InvoiceNumber": "110",
            "InvoiceDate": "14/01/2018",
            "DueDate": "15/01/2018",
            "BookingCode": "0875",
            "Room": "Superior Double",
            "TotalStayCount": "1",
            "TotalStayAmount": "$150",
            "CheckIn": "14/01/2018",
            "CheckOut": "15/01/2018",
            "CustomerDetails": "JOHNY SMITH\nR2, AVENUE DU MAROC\n123456",
            "DepositNow": "USD $20.90",
            "TaxVAT": "USD $19",
            "TotalAmount": "USD $209",
        }
    )
])
def test_validate_invoice_details(page, username, password, expected_details):
    """Valida que os detalhes da fatura estão corretos, mesmo abrindo em uma nova aba."""
    # URL da aplicação
    base_url = "https://automation-sandbox-python-mpywqjbdza-uc.a.run.app"

    # Inicializa a página de login
    login_page = LoginPage(page)
    login_page.navigate_to(base_url)
    login_page.login(username, password)

    # Espera a nova aba abrir após clicar no link "Invoice Details"
    with page.context.expect_page() as new_page_info:
        page.locator("text=Invoice Details").first.click()
    new_page = new_page_info.value

    # Aguarda a nova aba carregar completamente
    new_page.wait_for_load_state()

    # Valida o nome do hotel
    assert new_page.locator("h4").text_content().strip() == expected_details["HotelName"], "Hotel Name does not match."

    # Valida o número da fatura
    invoice_header = new_page.locator("h6").text_content().strip()
    assert f"Invoice #{expected_details['InvoiceNumber']} details" in invoice_header, "Invoice Number does not match."

    # Valida a data da fatura e a data de vencimento
    assert new_page.locator("li:has-text('Invoice Date:')").text_content().strip().endswith(expected_details["InvoiceDate"]), "Invoice Date does not match."
    assert new_page.locator("li:has-text('Due Date:')").text_content().strip().endswith(expected_details["DueDate"]), "Due Date does not match."

    # Valida os detalhes da reserva
    table_rows = new_page.locator("table").nth(0).locator("tr")
    assert table_rows.nth(0).locator("td").nth(1).text_content().strip() == expected_details["BookingCode"], "Booking Code does not match."
    assert table_rows.nth(1).locator("td").nth(1).text_content().strip() == expected_details["Room"], "Room does not match."
    assert table_rows.nth(2).locator("td").nth(1).text_content().strip() == expected_details["TotalStayCount"], "Total Stay Count does not match."
    assert table_rows.nth(3).locator("td").nth(1).text_content().strip() == expected_details["TotalStayAmount"], "Total Stay Amount does not match."
    assert table_rows.nth(4).locator("td").nth(1).text_content().strip() == expected_details["CheckIn"], "Check-In date does not match."
    assert table_rows.nth(5).locator("td").nth(1).text_content().strip() == expected_details["CheckOut"], "Check-Out date does not match."

    # Captura o HTML bruto do elemento
    customer_details_raw = new_page.locator("//h5[text()='Customer Details']/following-sibling::div").inner_html().strip()

    # Substitui as tags <br> por \n para refletir as quebras de linha
    customer_details = customer_details_raw.replace("<br />", "\n").replace("<br>", "\n").strip()

    # Verifica se o texto capturado corresponde ao esperado
    assert customer_details == expected_details["CustomerDetails"], f"Customer Details do not match: {customer_details}"



    # Valida os detalhes de faturamento
    billing_rows = new_page.locator("table").nth(1).locator("tr").nth(1).locator("td")
    assert billing_rows.nth(0).text_content().strip() == expected_details["DepositNow"], "Deposit Now does not match."
    assert billing_rows.nth(1).text_content().strip() == expected_details["TaxVAT"], "Tax & VAT does not match."
    assert billing_rows.nth(2).text_content().strip() == expected_details["TotalAmount"], "Total Amount does not match."
