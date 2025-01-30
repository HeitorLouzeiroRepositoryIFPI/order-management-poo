import unittest

from database.database import Database


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configura o banco de dados em memória para testes
        # Usa um banco de dados em memória
        cls.db = Database(db_name=':memory:')

    @classmethod
    def tearDownClass(cls):
        cls.db.conn.close()  # Feche apenas ao final de todos os testes

    def test_create_tables(self):
        # Verifica se as tabelas foram criadas corretamente
        tabelas = self.db.fetch_data(
            "SELECT name FROM sqlite_master WHERE type='table'")
        tabelas_esperadas = ['produtos', 'clientes',
                             'pedidos', 'pagamentos', 'entregas']
        for tabela in tabelas_esperadas:
            self.assertIn((tabela,), tabelas)

    def test_insert_cliente(self):
        # Testa a inserção de um cliente
        self.db.execute_query(
            "INSERT INTO clientes (nome, endereco) VALUES (?, ?)",
            ("Maria Silva", "Rua das Flores, 456")
        )
        clientes = self.db.fetch_data("SELECT nome, endereco FROM clientes")
        self.assertIn(("Maria Silva", "Rua das Flores, 456"), clientes)

    def test_insert_produto(self):
        # Testa a inserção de um produto
        self.db.execute_query(
            "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
            ("Notebook", 3500.00)
        )
        produtos = self.db.fetch_data("SELECT nome, preco FROM produtos")
        self.assertIn(("Notebook", 3500.00), produtos)

    def test_insert_pedido(self):
        # Testa a inserção de um pedido
        self.db.execute_query(
            "INSERT INTO clientes (nome, endereco) VALUES (?, ?)",
            ("João Silva", "Rua das Árvores, 123")
        )
        cliente_id = self.db.fetch_data(
            "SELECT id FROM clientes WHERE nome = 'João Silva'")[0][0]

        self.db.execute_query(
            "INSERT INTO pedidos (cliente_id, status, valor_total) VALUES (?, ?, ?)",
            (cliente_id, "Aguardando Pagamento", 100.00)
        )
        pedidos = self.db.fetch_data(
            "SELECT cliente_id, status, valor_total FROM pedidos")
        self.assertIn((cliente_id, "Aguardando Pagamento", 100.00), pedidos)


if __name__ == '__main__':
    unittest.main()
