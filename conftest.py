import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://opensource-demo.orangehrmlive.com/"

@pytest.fixture(scope="function")
def page(request):
    # Dossier pour chaque trace par test
    trace_path = f"traces/{request.node.name}.zip"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless pour CI/CD
        context = browser.new_context()

        page = context.new_page()

        # Commencer la trace
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        yield page

        # Stop trace et sauvegarde
        context.tracing.stop(path=trace_path)
        browser.close()
