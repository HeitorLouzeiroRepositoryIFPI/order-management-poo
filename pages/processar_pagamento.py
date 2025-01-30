import streamlit as st

from models import Pagamento
from utils.db_utils import execute_query, fetch_data


def show():
    st.subheader("Processamento de Pagamento")

    pedidos = fetch_data("""
        SELECT p.id, c.nome, p.valor_total 
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.status = 'Aguardando Pagamento'
    """)

    if pedidos:
        pedido_id = st.selectbox(
            "Selecione o pedido",
            options=[p[0] for p in pedidos],
            format_func=lambda x: next(
                f"Pedido #{p[0]} - {p[1]} (R${p[2]:.2f})" for p in pedidos if p[0] == x)
        )

        metodo = st.radio(
            "Método de pagamento",
            options=["Cartão", "Boleto", "Pix"]
        )

        if st.button("Processar Pagamento"):
            pagamento = Pagamento(pedido_id, metodo)
            status = pagamento.processar_pagamento()

            if status == "Aprovado":
                execute_query(
                    "UPDATE pedidos SET status = 'Pago' WHERE id = ?", (pedido_id,))
                st.success("Pagamento aprovado! Pedido liberado para envio.")
            else:
                st.error("Pagamento recusado. Tente outro método.")
    else:
        st.info("Nenhum pedido aguardando pagamento.")
