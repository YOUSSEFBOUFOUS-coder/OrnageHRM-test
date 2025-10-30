import pytest
from playwright.sync_api import sync_playwright
import os

# Récupère le navigateur depuis la variable d'environnement
BROWSER = os.getenv("BROWSER", "chromium")  # chromium par défaut

@pytest.fixture(scope="function")
def page(request):
    test_name = request.node.name  # nom du test en cours
    trace_dir = f"traces/{BROWSER}/{test_name}"  # dossier pour la trace

    with sync_playwright() as p:
        browser_type = getattr(p, BROWSER)
        browser = browser_type.launch(headless=True)  # mode headless pour CI
        context = browser.new_context(record_video_dir=None, record_trace_dir=trace_dir)
        page = context.new_page()
        
        # Active l'enregistrement de trace
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        yield page

        # Arrête et enregistre la trace
        context.tracing.stop(path=f"{trace_dir}.zip")
        context.close()
        browser.close()
