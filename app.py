import streamlit as st
from styles.styles import load_css

from pages import (cadastrar_cliente, cadastrar_produto, consultar_pedidos,
                   criar_pedido, gerenciar_entrega, processar_pagamento)

# Configuração inicial do CSS e navbar
st.set_page_config(page_title="Sistema de Pedidos", layout="wide")

# Carrega o CSS personalizado
load_css()

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

# ------ Roteamento das Páginas ------
if st.session_state.menu == "Cadastrar Cliente":
    cadastrar_cliente.show()

elif st.session_state.menu == "Cadastrar Produto":
    cadastrar_produto.show()

elif st.session_state.menu == "Criar Pedido":
    criar_pedido.show()

elif st.session_state.menu == "Processar Pagamento":
    processar_pagamento.show()

elif st.session_state.menu == "Gerenciar Entrega":
    gerenciar_entrega.show()

elif st.session_state.menu == "Consultar Pedidos":
    consultar_pedidos.show()
