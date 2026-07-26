import streamlit as st

from src.ui import renderizar_menu, shell


def main() -> None:
    ctx = shell("LabVida - Home", layout="wide")
    renderizar_menu(ctx["usuario_id"])

    user = ctx["user"]

    st.title("LabVida")
    st.caption(f"Olá, {user['name']}")

    st.divider()

    st.write("Bem-vindo ao LabVida!")
    st.info(
        "Utilize o menu lateral para navegar entre os módulos do ERP. "
        "As opções exibidas correspondem ao seu perfil de acesso."
    )


if __name__ == "__main__":
    main()
