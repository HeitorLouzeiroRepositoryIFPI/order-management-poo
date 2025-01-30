import unittest

from database.database import Database
from models import Cliente, Pedido, Produto


class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configura o banco de dados em memória para testes
        cls.db = Database(db_name=':memory:')
        cls.db.create_tables()  # Garante que as tabelas sejam criadas antes dos testes

    def test_cliente(self):
        # Testa a criação e salvamento de um cliente
        cliente = Cliente("Ana Maria", "Rua dos Testes, 789")
        cliente.salvar()
        clientes = self.db.fetch_data("SELECT nome, endereco FROM clientes")
        self.assertIn(("Ana Maria", "Rua dos Testes, 789"), clientes)

    def test_produto(self):
        # Testa a criação e salvamento de um produto
        produto = Produto("Smartphone", 1500.00)
        produto.salvar()
        produtos = self.db.fetch_data("SELECT nome, preco FROM produtos")
        self.assertIn(("Smartphone", 1500.00), produtos)

    def test_produto_preco_negativo(self):
        # Testa a validação de preço negativo para um produto
        with self.assertRaises(ValueError):
            Produto("TV 4K", -500.00).salvar()

    def test_pedido(self):
        # Testa a criação e salvamento de um pedido
        cliente = Cliente("Carlos Silva", "Rua dos Pedidos, 123")
        cliente.salvar()
        cliente_id = self.db.fetch_data(
            "SELECT id FROM clientes WHERE nome = 'Carlos Silva'")[0][0]

        pedido = Pedido(cliente_id, valor_total=200.00)
        pedido.salvar()
        pedidos = self.db.fetch_data(
            "SELECT cliente_id, valor_total FROM pedidos")
        self.assertIn((cliente_id, 200.00), pedidos)

    def test_pedido_sem_cliente(self):
        # Testa a criação de um pedido sem um cliente associado
        with self.assertRaises(Exception):
            Pedido(None, valor_total=300.00).salvar()

    def test_pedido_valor_zero(self):
        # Testa se um pedido com valor total zero pode ser salvo
        cliente = Cliente("Mariana Oliveira", "Rua das Compras, 456")
        cliente.salvar()
        cliente_id = self.db.fetch_data(
            "SELECT id FROM clientes WHERE nome = 'Mariana Oliveira'")[0][0]

        with self.assertRaises(ValueError):
            Pedido(cliente_id, valor_total=0).salvar()

    @classmethod
    def tearDownClass(cls):
        # Fecha a conexão com o banco de dados
        cls.db.close_connection()


if __name__ == '__main__':
    unittest.main()
