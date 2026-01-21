import sqlite3

class Database:
    def __init__(self, db_name="inventario.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        """)
        self.conn.commit()

    def inserir(self, nome, qtd, preco):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, qtd, preco))
        self.conn.commit()

    def selecionar_todos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()

    def deletar(self, id_item):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_item,))
        self.conn.commit()

    def atualizar(self, id_item, nome, qtd, preco):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE produtos 
            SET nome = ?, quantidade = ?, preco = ? 
            WHERE id = ?
        """, (nome, qtd, preco, id_item))
        self.conn.commit()

    def limpar_tudo(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM produtos")
        self.conn.commit()

    def buscar_produtos(self, termo):
        cursor = self.conn.cursor()
        # O % permite buscar qualquer texto antes ou depois do termo
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{termo}%",))
        return cursor.fetchall()