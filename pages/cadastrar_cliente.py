import streamlit as st

from models import Cliente


def show():
    with st.form("cliente_form"):
        st.subheader("Novo Cliente")
        nome = st.text_input("Nome completo")
        endereco = st.text_area("Endereço de entrega")

        if st.form_submit_button("Salvar Cliente"):
            cliente = Cliente(nome, endereco)
            cliente.salvar()
            st.success("Cliente cadastrado com sucesso!")
