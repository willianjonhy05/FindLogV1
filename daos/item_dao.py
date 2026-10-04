from database.sqlitedb import SQLiteDB


class ItemDAO:

    def add_item(self, item):
        db = SQLiteDB()
        return db.execute("""
            INSERT INTO item
            (cor, tamanho, data, foto, categoria,
             onde_encontrado, quem_encontrou, onde_guardado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.cor, item.tamanho, item.data, item.foto,
            item.categoria.codigo, item.onde_encontrado,
            item.quem_encontrou, item.onde_guardado
        ))

    def get_itens(self):
        return SQLiteDB().execute("SELECT * FROM item")