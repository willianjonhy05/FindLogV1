class CategoriaDAO:

    def add_categoria(self, categoria):
        from main import supabase
        
        dados = {
            "codigo": categoria.codigo,
            "nome": categoria.nome,
            "slug": categoria.slug,
            "descricao": categoria.descricao,
            "ativa": bool(categoria.ativa)
        }
        
        try:
            resposta = supabase.table("categorias").insert(dados).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao adicionar categoria: {erro}")
            return None

    def get_categorias(self):
        from main import supabase
        from models.categoria import Categoria
        
        response = supabase.table('categorias').select("*").execute()
        categorias = []
        
        data_rows = response.data if hasattr(response, 'data') else response
        
        for row in data_rows:
            # Passamos o dicionário row diretamente, mantendo o padrão da Instituição
            categoria = Categoria(data=row)
            categorias.append(categoria)

        return categorias


    def get_categorias_ativas(self):
        from main import supabase
        from models.categoria import Categoria

        response = supabase.table('categorias').select("codigo, nome").eq("ativa", True).execute()
        return response.data if hasattr(response, 'data') else response
    

    def get_categoria_by_codigo(self, codigo):
        from main import supabase
        from models.categoria import Categoria
        
        try:
            resposta = supabase.table("categorias").select("*").eq("codigo", codigo).execute()
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta
            
            if data_rows and len(data_rows) > 0:
                return Categoria(data=data_rows[0])
                
        except Exception as erro:
            print(f"Erro ao buscar categoria por código: {erro}")
            
        return None

    def get_categoria_by_slug(self, slug):
        """Busca uma categoria específica pelo slug para garantir unicidade."""
        from main import supabase
        from models.categoria import Categoria
        
        try:
            resposta = supabase.table('categorias').select("*").eq("slug", slug).execute()
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta
            
            if data_rows and len(data_rows) > 0:
                return Categoria(data=data_rows[0])
        except Exception as erro:
            print(f"Erro ao buscar categoria por slug: {erro}")
            
        return None

    def atualizar_categoria(self, categoria):
        from main import supabase
        
        # O slug NÃO é atualizado aqui porque ele é imutável após a criação
        dados = {
            "nome": categoria.nome,
            "descricao": categoria.descricao,
            "ativa": bool(categoria.ativa)
        }
        
        try:
            resposta = supabase.table("categorias").update(dados).eq("codigo", categoria.codigo).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao atualizar categoria: {erro}")
            return None

    def deletar_categoria(self, codigo):
        from main import supabase
        
        try:
            resposta = supabase.table("categorias").delete().eq("codigo", codigo).execute()
            return resposta.data if hasattr(resposta, 'data') else resposta
        except Exception as erro:
            print(f"Erro ao deletar categoria: {erro}")
            return None

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