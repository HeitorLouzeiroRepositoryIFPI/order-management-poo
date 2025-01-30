from database.database import Database

db = Database()


class Produto:
    def __init__(self, nome, preco, id=None):
        self.id = id
        self.nome = nome
        self.preco = preco

    def salvar(self):
        query = "INSERT INTO produtos (nome, preco) VALUES (?, ?)"
        self.id = db.execute_query(query, (self.nome, self.preco))


class Cliente:
    def __init__(self, nome, endereco, id=None):
        self.id = id
        self.nome = nome
        self.endereco = endereco

    def salvar(self):
        query = "INSERT INTO clientes (nome, endereco) VALUES (?, ?)"
        self.id = db.execute_query(query, (self.nome, self.endereco))


class Pedido:
    def __init__(self, cliente_id, status="Aguardando Pagamento", valor_total=0, id=None):
        self.id = id
        self.cliente_id = cliente_id
        self.status = status
        self.valor_total = valor_total

    def salvar(self):
        query = "INSERT INTO pedidos (cliente_id, status, valor_total) VALUES (?, ?, ?)"
        self.id = db.execute_query(
            query, (self.cliente_id, self.status, self.valor_total))


class Pagamento:
    def __init__(self, pedido_id, metodo, status="Aguardando", id=None):
        self.id = id
        self.pedido_id = pedido_id
        self.metodo = metodo
        self.status = status

    def processar_pagamento(self):
        # Simulação de processamento
        self.status = "Aprovado" if self.metodo in [
            "Cartão", "Pix"] else "Aguardando"
        query = "INSERT INTO pagamentos (pedido_id, metodo, status) VALUES (?, ?, ?)"
        self.id = db.execute_query(
            query, (self.pedido_id, self.metodo, self.status))
        return self.status


class Entrega:
    def __init__(self, pedido_id, status="Aguardando Envio", codigo_rastreamento=None, id=None):
        self.id = id
        self.pedido_id = pedido_id
        self.status = status
        self.codigo_rastreamento = codigo_rastreamento

    def iniciar_entrega(self):
        self.status = "Em Transporte"
        query = "INSERT INTO entregas (pedido_id, status) VALUES (?, ?)"
        self.id = db.execute_query(query, (self.pedido_id, self.status))

    def finalizar_entrega(self):
        self.status = "Entregue"
        query = "UPDATE entregas SET status = ? WHERE pedido_id = ?"
        db.execute_query(query, (self.status, self.pedido_id))
