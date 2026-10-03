from database.sqlitedb import SQLiteDB


class CategoriaDAO:

    def add_categoria(self, categoria):
        db = SQLiteDB()
        return db.execute("""
            INSERT INTO categoria (nome, codigo, descricao)
            VALUES (?, ?, ?)
        """, (
            categoria.nome,
            categoria.codigo,
            categoria.descricao
        ))

    def get_categorias(self):
        db = SQLiteDB()
        return db.execute("""
            SELECT * FROM categoria
        """)

    def get_categoria_by_codigo(self, codigo):
        db = SQLiteDB()
        return db.execute("""
            SELECT * FROM categoria
            WHERE codigo = ?
        """, (codigo,))

    def deletar_categoria(self, codigo):
        db = SQLiteDB()
        return db.execute("""
            DELETE FROM categoria
            WHERE codigo = ?
        """, (codigo,))

    def atualizar_categoria(self, categoria):
        db = SQLiteDB()
        return db.execute("""
            UPDATE categoria
            SET nome = ?, descricao = ?
            WHERE codigo = ?
        """, (
            categoria.nome,
            categoria.descricao,
            categoria.codigo
        ))