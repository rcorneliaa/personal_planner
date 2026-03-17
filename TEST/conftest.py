# conftest.py
import pytest
from pytest_html import extras

@pytest.fixture
def log_extra(request):
    """Fixture pentru a adăuga mesaje custom în raportul HTML."""
    def _log(message: str):
        # obține obiectul de raport html din request
        html = request.config.pluginmanager.getplugin("html")
        if html is not None:
            # folosim hook-ul pytest_html_results_table_row
            if not hasattr(request.node, "extras"):
                request.node.extras = []
            request.node.extras.append(extras.text(message))
    return _log