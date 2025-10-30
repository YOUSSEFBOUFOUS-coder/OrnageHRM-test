import pytest
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

@pytest.fixture(scope="function")
def page(request):  # <-- 'request' permet de connaître le nom du test
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # 📁 Création des dossiers si inexistants
        os.makedirs("videos", exist_ok=True)
        os.makedirs("traces", exist_ok=True)

        # 🎬 Nom du test + horodatage
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 🎥 Enregistrement vidéo
        context = browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720}
        )

        # 🧠 Démarrage du trace
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        yield page

        # 💾 Sauvegarde du trace propre à chaque test
        trace_path = f"traces/trace_{test_name}_{timestamp}.zip"
        context.tracing.stop(path=trace_path)

        # 🔚 Fermeture du contexte et navigateur
        context.close()
        browser.close()
