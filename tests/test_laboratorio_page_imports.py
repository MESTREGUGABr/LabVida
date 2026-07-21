import ast
import importlib
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent


def test_laboratorio_pages_import_only_existing_symbols() -> None:
    service_modules = {}

    for page_path in (PROJECT_ROOT / "pages").glob("laboratorio_*.py"):
        tree = ast.parse(page_path.read_text(), filename=str(page_path))

        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or not node.module:
                continue

            if node.module not in service_modules:
                service_modules[node.module] = importlib.import_module(node.module)

            module = service_modules[node.module]
            missing = [alias.name for alias in node.names if not hasattr(module, alias.name)]
            assert not missing, f"{page_path.name} importa símbolos ausentes: {missing}"
