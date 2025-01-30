import streamlit as st

from models import *

st.title("Sistema de Gestão de Pedidos")

menu = st.sidebar.selectbox("Menu", [
    "Cadastrar Cliente",
    "Cadastrar Produto",
    "Criar Pedido",
    "Processar Pagamento",
    "Gerenciar Entrega",
    "Consultar Pedidos"
])

if menu == "Cadastrar Cliente":
    st.header("Cadastrar Novo Cliente")
    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")
    if st.button("Salvar Cliente"):
        cliente = Cliente(nome, endereco)
        cliente.salvar()
        st.success("Cliente cadastrado com sucesso!")

elif menu == "Cadastrar Produto":
    st.header("Cadastrar Novo Produto")
    nome = st.text_input("Nome do Produto")
    preco = st.number_input("Preço", min_value=0.0)
    if st.button("Salvar Produto"):
        produto = Produto(nome, preco)
        produto.salvar()
        st.success("Produto cadastrado com sucesso!")

elif menu == "Criar Pedido":
    st.header("Criar Novo Pedido")
    clientes = db.fetch_data("SELECT id, nome FROM clientes")
    cliente_id = st.selectbox("Selecione o Cliente", [c[0] for c in clientes])

    produtos = db.fetch_data("SELECT id, nome, preco FROM produtos")
    produtos_selecionados = st.multiselect("Selecione os Produtos", produtos)

    if st.button("Criar Pedido"):
        valor_total = sum(p[2] for p in produtos_selecionados)
        pedido = Pedido(cliente_id, valor_total=valor_total)
        pedido.salvar()
        st.success(
            f"Pedido #{pedido.id} criado com valor total: R${valor_total:.2f}")

elif menu == "Processar Pagamento":
    st.header("Processar Pagamento")
    pedidos = db.fetch_data(
        "SELECT id FROM pedidos WHERE status = 'Aguardando Pagamento'")
    pedido_id = st.selectbox("Selecione o Pedido", [p[0] for p in pedidos])
    metodo = st.selectbox("Método de Pagamento", ["Cartão", "Boleto", "Pix"])

    if st.button("Processar"):
        pagamento = Pagamento(pedido_id, metodo)
        status = pagamento.processar_pagamento()
        if status == "Aprovado":
            db.execute_query(
                "UPDATE pedidos SET status = 'Pago' WHERE id = ?", (pedido_id,))
        st.success(f"Pagamento {status}")

elif menu == "Gerenciar Entrega":
    st.header("Gerenciar Entrega")
    pedidos = db.fetch_data("SELECT id FROM pedidos WHERE status = 'Pago'")
    pedido_id = st.selectbox("Selecione o Pedido para Entrega", [
                             p[0] for p in pedidos])

    if st.button("Iniciar Entrega"):
        entrega = Entrega(pedido_id)
        entrega.iniciar_entrega()
        st.success("Entrega iniciada!")

    if st.button("Finalizar Entrega"):
        entrega = Entrega(pedido_id)
        entrega.finalizar_entrega()
        db.execute_query(
            "UPDATE pedidos SET status = 'Entregue' WHERE id = ?", (pedido_id,))
        st.success("Entrega finalizada!")

elif menu == "Consultar Pedidos":
    st.header("Consultar Pedidos")
    pedidos = db.fetch_data('''
        SELECT p.id, c.nome, p.valor_total, p.status
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
    ''')

    for pedido in pedidos:
        st.write(
            f"Pedido #{pedido[0]} - Cliente: {pedido[1]} - Valor: R${pedido[2]:.2f} - Status: {pedido[3]}")
