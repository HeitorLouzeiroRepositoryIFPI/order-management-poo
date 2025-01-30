import sqlite3


class Database:
    _instance = None

    def __new__(cls, db_name='database/ecommerce.db'):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(
                db_name, check_same_thread=False)
            cls._instance.create_tables()
        return cls._instance

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                status TEXT,
                valor_total REAL,
                FOREIGN KEY(cliente_id) REFERENCES clientes(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER,
                metodo TEXT,
                status TEXT,
                FOREIGN KEY(pedido_id) REFERENCES pedidos(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entregas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER,
                status TEXT,
                codigo_rastreamento TEXT,
                FOREIGN KEY(pedido_id) REFERENCES pedidos(id)
            )
        ''')

        self.conn.commit()

    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid

    def fetch_data(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
