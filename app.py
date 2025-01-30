import streamlit as st

from models import *

# Configuração inicial do CSS e navbar
st.set_page_config(page_title="Sistema de Pedidos", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    /* Estilos da navbar */
    .nav-bar {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 1rem;
    }
    
    /* Estilos dos botões */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s ease;
        text-align: left;
    }
    
    .stButton>button:hover {
        transform: translateX(5px);
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Estilo do título */
    .header {
        font-size: 2.5em !important;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ========== Sidebar (Navbar) ==========
with st.sidebar:
    st.markdown("## Navegação", unsafe_allow_html=True)
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)

    # Ícones e labels dos botões
    menu_options = {
        "Cadastrar Cliente": "👤 Cadastrar Cliente",
        "Cadastrar Produto": "📦 Cadastrar Produto",
        "Criar Pedido": "🛒 Criar Pedido",
        "Processar Pagamento": "💳 Processar Pagamento",
        "Gerenciar Entrega": "🚚 Gerenciar Entrega",
        "Consultar Pedidos": "📋 Consultar Pedidos"
    }

    # Inicializa o estado do menu
    if 'menu' not in st.session_state:
        st.session_state.menu = "Cadastrar Cliente"

    # Cria os botões de navegação
    for key, value in menu_options.items():
        if st.button(
            value,
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if st.session_state.menu == key else "secondary"
        ):
            st.session_state.menu = key

    st.markdown('</div>', unsafe_allow_html=True)

# ========== Conteúdo Principal ==========
st.markdown('<div class="header">📦 Sistema de Gestão de Pedidos</div>',
            unsafe_allow_html=True)

# ------ Cadastrar Cliente ------
if st.session_state.menu == "Cadastrar Cliente":
    with st.form("cliente_form"):
        st.subheader("Novo Cliente")
        nome = st.text_input("Nome completo")
        endereco = st.text_area("Endereço de entrega")

        if st.form_submit_button("Salvar Cliente"):
            cliente = Cliente(nome, endereco)
            cliente.salvar()
            st.success("Cliente cadastrado com sucesso!")

# ------ Cadastrar Produto ------
elif st.session_state.menu == "Cadastrar Produto":
    with st.form("produto_form"):
        st.subheader("Novo Produto")
        nome = st.text_input("Nome do produto")
        preco = st.number_input("Preço unitário", min_value=0.0, format="%.2f")

        if st.form_submit_button("Salvar Produto"):
            produto = Produto(nome, preco)
            produto.salvar()
            st.success("Produto cadastrado com sucesso!")

# ------ Criar Pedido ------
elif st.session_state.menu == "Criar Pedido":
    st.subheader("Novo Pedido")

    # Seleção de cliente
    clientes = db.fetch_data("SELECT id, nome FROM clientes")
    cliente_id = st.selectbox(
        "Selecione o cliente",
        options=[c[0] for c in clientes],
        format_func=lambda x: next(c[1] for c in clientes if c[0] == x)
    )

    # Seleção de produtos
    produtos = db.fetch_data("SELECT id, nome, preco FROM produtos")
    produtos_selecionados = st.multiselect(
        "Selecione os produtos",
        options=produtos,
        format_func=lambda x: f"{x[1]} - R${x[2]:.2f}"
    )

    if st.button("Finalizar Pedido"):
        valor_total = sum(p[2] for p in produtos_selecionados)
        pedido = Pedido(cliente_id, valor_total=valor_total)
        pedido.salvar()
        st.success(f"Pedido #{pedido.id} criado (Total: R${valor_total:.2f})")

# ------ Processar Pagamento ------
elif st.session_state.menu == "Processar Pagamento":
    st.subheader("Processamento de Pagamento")

    pedidos = db.fetch_data("""
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
                db.execute_query(
                    "UPDATE pedidos SET status = 'Pago' WHERE id = ?", (pedido_id,))
                st.success("Pagamento aprovado! Pedido liberado para envio.")
            else:
                st.error("Pagamento recusado. Tente outro método.")
    else:
        st.info("Nenhum pedido aguardando pagamento.")

# ------ Gerenciar Entrega ------
elif st.session_state.menu == "Gerenciar Entrega":
    st.subheader("Gestão de Entregas")

    pedidos = db.fetch_data("""
        SELECT p.id, c.nome, p.valor_total 
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.status = 'Pago'
    """)

    if pedidos:
        pedido_id = st.selectbox(
            "Selecione o pedido para envio",
            options=[p[0] for p in pedidos],
            format_func=lambda x: next(
                f"Pedido #{p[0]} - {p[1]} (R${p[2]:.2f})" for p in pedidos if p[0] == x)
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Iniciar Entrega"):
                entrega = Entrega(pedido_id)
                entrega.iniciar_entrega()
                db.execute_query(
                    "UPDATE pedidos SET status = 'Enviado' WHERE id = ?", (pedido_id,))
                st.success("Entrega iniciada com sucesso!")

        with col2:
            if st.button("Finalizar Entrega"):
                entrega = Entrega(pedido_id)
                entrega.finalizar_entrega()
                db.execute_query(
                    "UPDATE pedidos SET status = 'Entregue' WHERE id = ?", (pedido_id,))
                st.success("Entrega finalizada com sucesso!")
    else:
        st.info("Nenhum pedido pronto para envio.")

# ------ Consultar Pedidos ------
elif st.session_state.menu == "Consultar Pedidos":
    st.subheader("Consulta de Pedidos")

    pedidos = db.fetch_data('''
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
