import streamlit as st

from models import Entrega
from utils.db_utils import fetch_data


def show():
    st.subheader("Gestão de Entregas")

    # Busca pedidos com informações de entrega
    dados = fetch_data("""
        SELECT 
            p.id,
            c.nome,
            p.valor_total,
            p.status,
            e.codigo_rastreamento,
            e.status as status_entrega
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        LEFT JOIN entregas e ON p.id = e.pedido_id
        WHERE p.status IN ('Pago', 'Enviado')
        ORDER BY p.id DESC
    """)

    if dados:
        # Cria a tabela interativa
        col1, col2, col3, col4, col5, col6 = st.columns([0.5, 2, 1, 1, 2, 1])
        with col1:
            st.markdown("**Pedido ID**")
        with col2:
            st.markdown("**Cliente**")
        with col3:
            st.markdown("**Valor**")
        with col4:
            st.markdown("**Status**")
        with col5:
            st.markdown("**Código Rastreio**")
        with col6:
            st.markdown("**Ações**")

        for pedido in dados:
            col1, col2, col3, col4, col5, col6 = st.columns(
                [0.5, 2, 1, 1, 2, 1])

            with col1:
                st.write(f"#{pedido[0]}")
            with col2:
                st.write(pedido[1])
            with col3:
                st.write(f"R${pedido[2]:.2f}")
            with col4:
                st.write(pedido[3])
            with col5:
                st.write(pedido[4] or "Gerar ao enviar")

            with col6:
                if pedido[3] == "Pago":
                    if st.button("🚚 Iniciar", key=f"iniciar_{pedido[0]}"):
                        entrega = Entrega(pedido[0])
                        entrega.iniciar_entrega()
                        st.rerun()

                elif pedido[3] == "Enviado":
                    if st.button("✅ Finalizar", key=f"finalizar_{pedido[0]}"):
                        entrega = Entrega(pedido[0])
                        entrega.finalizar_entrega()
                        st.rerun()
    else:
        st.info("Nenhum pedido requer ação de entrega no momento.")
