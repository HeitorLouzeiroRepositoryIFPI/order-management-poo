import streamlit as st

from models import Produto


def show():
    with st.form("produto_form"):
        st.subheader("Novo Produto")
        nome = st.text_input("Nome do produto")
        preco = st.number_input("Preço unitário", min_value=0.0, format="%.2f")

        if st.form_submit_button("Salvar Produto"):
            produto = Produto(nome, preco)
            produto.salvar()
            st.success("Produto cadastrado com sucesso!")
