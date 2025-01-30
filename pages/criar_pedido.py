import streamlit as st

from models import Pedido
from utils.db_utils import fetch_data


def show():
    st.subheader("Novo Pedido")

    # Seleção de cliente
    clientes = fetch_data("SELECT id, nome FROM clientes")
    cliente_id = st.selectbox(
        "Selecione o cliente",
        options=[c[0] for c in clientes],
        format_func=lambda x: next(c[1] for c in clientes if c[0] == x)
    )

    # Seleção de produtos
    produtos = fetch_data("SELECT id, nome, preco FROM produtos")
    produtos_selecionados = st.multiselect(
        "Selecione os produtos",
        options=produtos,
        format_func=lambda x: f"{x[1]} - R${x[2]:.2f}"
    )

    if st.button("Finalizar Pedido"):
        if not produtos_selecionados:
            st.error("Selecione pelo menos um produto.")
            return

        valor_total = sum(p[2] for p in produtos_selecionados)
        pedido = Pedido(cliente_id, valor_total=valor_total)
        pedido.salvar()
        st.success(f"Pedido #{pedido.id} criado (Total: R${valor_total:.2f})")
