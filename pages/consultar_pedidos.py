import streamlit as st

from utils.db_utils import fetch_data


def show():
    st.subheader("Consulta de Pedidos")

    pedidos = fetch_data('''
        SELECT p.id, c.nome, p.valor_total, p.status 
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.id DESC
    ''')

    if pedidos:
        for pedido in pedidos:
            status_color = {
                "Aguardando Pagamento": "🔴",
                "Pago": "🟡",
                "Enviado": "🟢",
                "Entregue": "✅"
            }.get(pedido[3], "⚪")

            st.markdown(f"""
            <div style="padding: 15px; border-radius: 10px; margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
                <b>Pedido #{pedido[0]}</b> - {status_color} {pedido[3]}
                <div style="margin-top: 5px; color: #666">
                    Cliente: {pedido[1]}<br>
                    Valor Total: R${pedido[2]:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum pedido registrado no sistema.")
