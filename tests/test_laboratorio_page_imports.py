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


def test_codebase_has_no_undefined_global_names() -> None:
    import builtins
    import symtable

    builtin_names = set(dir(builtins))
    search_dirs = [PROJECT_ROOT / "pages", PROJECT_ROOT / "src"]

    for base_dir in search_dirs:
        for py_path in base_dir.rglob("*.py"):
            code = py_path.read_text()
            st = symtable.symtable(code, str(py_path), "exec")
            top_globals = set(st.get_identifiers())

            undefined = set()

            def check(t):
                for sym in t.get_symbols():
                    if sym.is_global() and not sym.is_declared_global():
                        name = sym.get_name()
                        if name not in top_globals and name not in builtin_names:
                            undefined.add(f"{t.get_name()}:{name}")
                for child in t.get_children():
                    check(child)

            check(st)
            assert not undefined, f"{py_path.relative_to(PROJECT_ROOT)} possui símbolos globais não definidos: {undefined}"


