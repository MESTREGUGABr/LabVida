from streamlit.testing.v1 import AppTest


def test_home_page_renders_labvida() -> None:
    app = AppTest.from_file("app.py")

    app.run()

    assert not app.exception
    assert app.title[0].value == "LabVida"
    assert app.caption[0].value == "ERP para laboratório de análises clínicas"
