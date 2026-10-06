from database.sqlitedb import SQLiteDB


class CategoriaDAO:

    def add_categoria(self, categoria):
        from main import supabase
        from models.categoria import Categoria
        
        dados = {
            "codigo": categoria.codigo,
            "nome": categoria.nome,
            "slug": categoria.slug,
            "descricao": categoria.descricao,
            "ativa": categoria.ativa 
        }
        
        resposta = supabase.table("categorias").insert(dados).execute()
        return resposta.data[0] if resposta.data else None

        # db = SQLiteDB()
        # return db.execute("""
        #     INSERT INTO categoria (nome, codigo, descricao)
        #     VALUES (?, ?, ?)
        # """, (
        #     categoria.nome,
        #     categoria.codigo,
        #     categoria.descricao
        # ))

    def get_categorias(self):
        from main import supabase
        from models.categoria import Categoria
        response = supabase.table('categorias').select("*").execute()
        categorias = []

        for row in response.data:
            categoria = Categoria(
                nome=linha['nome'],
                descricao=linha['descricao'],
                codigo=linha['codigo'],
                slug=linha['slug']
            )
            categoria.ativa = bool(linha['ativa'])
            categorias.append(categoria)

        return categorias

        # db = SQLiteDB()
        # return db.execute("""
        #     SELECT * FROM categoria
        # """)

    def get_categoria_by_codigo(self, codigo):
        from main import supabase
        from models.categoria import Categoria
        
        try:
            resposta = supabase.table("categorias").select("*").eq("codigo", codigo).execute()
            dados = resposta.data
            
            if dados and len(dados) > 0:
                linha = dados[0]
                cat = Categoria(
                    nome=linha['nome'],
                    descricao=linha['descricao'],
                    codigo=linha['codigo'],
                    slug=linha['slug']
                )
                cat.ativa = bool(linha['ativa'])
                return cat
                
        except Exception as erro:
            print(f"Erro ao buscar categoria por código: {erro}")
            
        return None

    def deletar_categoria(self, codigo):
        from main import supabase
        
        try:
            resposta = supabase.table("categorias").delete().eq("codigo", codigo).execute()
            return resposta.data
        except Exception as erro:
            print(f"Erro ao deletar categoria: {erro}")
            return None

    def atualizar_categoria(self, categoria):
        from main import supabase
        
        dados = {
            "nome": categoria.nome,
            "descricao": categoria.descricao,
            "slug": categoria.slug, # Atualizamos o slug caso o nome mude
            "ativa": categoria.ativa
        }
        
        try:
            resposta = supabase.table("categorias").update(dados).eq("codigo", categoria.codigo).execute()
            return resposta.data
        except Exception as erro:
            print(f"Erro ao atualizar categoria: {erro}")
            return None


    # def get_categoria_by_codigo(self, codigo):
    #     db = SQLiteDB()
    #     return db.execute("""
    #         SELECT * FROM categoria
    #         WHERE codigo = ?
    #     """, (codigo,))

    # def deletar_categoria(self, codigo):
    #     db = SQLiteDB()
    #     return db.execute("""
    #         DELETE FROM categoria
    #         WHERE codigo = ?
    #     """, (codigo,))

    # def atualizar_categoria(self, categoria):
    #     db = SQLiteDB()
    #     return db.execute("""
    #         UPDATE categoria
    #         SET nome = ?, descricao = ?
    #         WHERE codigo = ?
    #     """, (
    #         categoria.nome,
    #         categoria.descricao,
    #         categoria.codigo
    #     ))

    def contar_total(self):
        from main import supabase
        try:
            resposta = supabase.table("categorias").select("*", count="exact", head=True).execute()
            return resposta.count if resposta.count is not None else 0
        except Exception as e:
            print(f"Erro ao contar total de categorias: {e}")
            return 0

    def contar_por_status(self, ativa):
        from main import supabase
        try:
            resposta = supabase.table("categorias").select("*", count="exact", head=True).eq("ativa", ativa).execute()
            return resposta.count if resposta.count is not None else 0
        except Exception as e:
            print(f"Erro ao contar categorias por status: {e}")
            return 0