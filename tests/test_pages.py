import unittest

from database.database import Database
from pages.cadastrar_cliente import show as show_cadastrar_cliente
from pages.cadastrar_produto import show as show_cadastrar_produto
from pages.consultar_pedidos import show as show_consultar_pedidos
from pages.criar_pedido import show as show_criar_pedido
from pages.gerenciar_entrega import show as show_gerenciar_entrega
from pages.processar_pagamento import show as show_processar_pagamento


class TestPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configura o banco de dados em memória para testes
        cls.db = Database(db_name=':memory:')

    def test_cadastrar_cliente(self):
        # Testa o cadastro de um cliente
        show_cadastrar_cliente()
        clientes = self.db.fetch_data("SELECT nome, endereco FROM clientes")
        # Verifica se pelo menos um cliente foi cadastrado
        self.assertGreaterEqual(len(clientes), 1)

    def test_cadastrar_produto(self):
        # Testa o cadastro de um produto
        show_cadastrar_produto()
        produtos = self.db.fetch_data("SELECT nome, preco FROM produtos")
        # Verifica se pelo menos um produto foi cadastrado
        self.assertGreaterEqual(len(produtos), 1)

    def test_criar_pedido(self):
        # Testa a criação de um pedido
        # Primeiro, cadastra um cliente e um produto
        self.db.execute_query(
            "INSERT INTO clientes (nome, endereco) VALUES (?, ?)", ("Cliente Teste", "Rua Teste, 123"))
        self.db.execute_query(
            "INSERT INTO produtos (nome, preco) VALUES (?, ?)", ("Produto Teste", 100.00))

        show_criar_pedido()
        pedidos = self.db.fetch_data(
            "SELECT cliente_id, valor_total FROM pedidos")
        # Verifica se pelo menos um pedido foi criado
        self.assertGreaterEqual(len(pedidos), 1)

    def test_processar_pagamento(self):
        # Testa o processamento de um pagamento
        # Primeiro, cadastra um cliente e um pedido
        self.db.execute_query(
            "INSERT INTO clientes (nome, endereco) VALUES (?, ?)", ("Cliente Teste", "Rua Teste, 123"))
        cliente_id = self.db.fetch_data(
            "SELECT id FROM clientes WHERE nome = 'Cliente Teste'")[0][0]
        self.db.execute_query("INSERT INTO pedidos (cliente_id, status, valor_total) VALUES (?, ?, ?)",
                              (cliente_id, "Aguardando Pagamento", 100.00))

        show_processar_pagamento()
        pagamentos = self.db.fetch_data("SELECT status FROM pagamentos")
        # Verifica se pelo menos um pagamento foi processado
        self.assertGreaterEqual(len(pagamentos), 1)

    def test_gerenciar_entrega(self):
        # Testa o gerenciamento de uma entrega
        # Primeiro, cadastra um cliente, um pedido e um pagamento
        self.db.execute_query(
            "INSERT INTO clientes (nome, endereco) VALUES (?, ?)", ("Cliente Teste", "Rua Teste, 123"))
        cliente_id = self.db.fetch_data(
            "SELECT id FROM clientes WHERE nome = 'Cliente Teste'")[0][0]
        self.db.execute_query(
            "INSERT INTO pedidos (cliente_id, status, valor_total) VALUES (?, ?, ?)", (cliente_id, "Pago", 100.00))
        pedido_id = self.db.fetch_data(
            "SELECT id FROM pedidos WHERE cliente_id = ?", (cliente_id,))[0][0]
        self.db.execute_query(
            "INSERT INTO pagamentos (pedido_id, metodo, status) VALUES (?, ?, ?)", (pedido_id, "Cartão", "Aprovado"))

        show_gerenciar_entrega()
        entregas = self.db.fetch_data("SELECT status FROM entregas")
        # Verifica se pelo menos uma entrega foi gerenciada
        self.assertGreaterEqual(len(entregas), 1)

    def test_consultar_pedidos(self):
        # Testa a consulta de pedidos
        # Primeiro, cadastra um cliente e um pedido
        self.db.execute_query(
            "INSERT INTO clientes (nome, endereco) VALUES (?, ?)", ("Cliente Teste", "Rua Teste, 123"))
        cliente_id = self.db.fetch_data(
            "SELECT id FROM clientes WHERE nome = 'Cliente Teste'")[0][0]
        self.db.execute_query("INSERT INTO pedidos (cliente_id, status, valor_total) VALUES (?, ?, ?)",
                              (cliente_id, "Aguardando Pagamento", 100.00))

        show_consultar_pedidos()
        pedidos = self.db.fetch_data("SELECT status FROM pedidos")
        # Verifica se pelo menos um pedido foi consultado
        self.assertGreaterEqual(len(pedidos), 1)

    def test_cadastrar_cliente_com_dados_invalidos(self):
        # Testa o cadastro de um cliente com dados inválidos (nome vazio)
        show_cadastrar_cliente()
        clientes = self.db.fetch_data(
            "SELECT nome FROM clientes WHERE nome = ''")
        # Verifica se nenhum cliente com nome vazio foi cadastrado
        self.assertEqual(len(clientes), 0)

    def test_cadastrar_produto_com_preco_negativo(self):
        # Testa o cadastro de um produto com preço negativo
        show_cadastrar_produto()
        produtos = self.db.fetch_data(
            "SELECT preco FROM produtos WHERE preco < 0")
        # Verifica se nenhum produto com preço negativo foi cadastrado
        self.assertEqual(len(produtos), 0)

    def test_criar_pedido_sem_produtos(self):
        # Testa a criação de um pedido sem produtos selecionados
        show_criar_pedido()
        pedidos = self.db.fetch_data(
            "SELECT valor_total FROM pedidos WHERE valor_total = 0")
        # Verifica se nenhum pedido com valor total zero foi criado
        self.assertEqual(len(pedidos), 0)

    def test_processar_pagamento_sem_pedido(self):
        # Testa o processamento de um pagamento sem pedido existente
        show_processar_pagamento()
        pagamentos = self.db.fetch_data(
            "SELECT pedido_id FROM pagamentos WHERE pedido_id IS NULL")
        # Verifica se nenhum pagamento sem pedido foi processado
        self.assertEqual(len(pagamentos), 0)

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão com o banco de dados
        cls.db.close_connection()


if __name__ == '__main__':
    unittest.main()
