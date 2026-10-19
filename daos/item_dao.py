class ItemDAO:

    def get_itens(self):
        from main import supabase
        from models.item import Item
        
        response = supabase.table('itens').select("*").execute()
        itens = []
        
        data_rows = response.data if hasattr(response, 'data') else response
        
        for row in data_rows:
            # Mapeia as colunas do banco para as chaves limpas que a classe Item espera
            row_data = row.copy()
            row_data["categoria"] = row.get("categoria_codigo")
            row_data["instituicao"] = row.get("instituicao_cnpj")
            row_data["onde_guardado"] = row.get("onde_guardado_codigo")
            row_data["quem_encontrou"] = row.get("quem_encontrou_username")
            row_data["dono"] = row.get("dono_username")
            
            item = Item(data=row_data)
            itens.append(item)
            
        return itens


    def get_itens_by_instituicao(self, cnpj):
        from main import supabase
        from models.item import Item

        response = supabase.table('itens').select("*").eq("instituicao_cnpj", cnpj).execute()
        itens = []

        data_rows = response.data if hasattr(response, 'data') else response

        for row in data_rows:
            # Mapeia as colunas do banco para as chaves limpas que a classe Item espera
            row_data = row.copy()
            row_data["categoria"] = row.get("categoria_codigo")
            row_data["instituicao"] = row.get("instituicao_cnpj")
            row_data["onde_guardado"] = row.get("onde_guardado_codigo")
            row_data["quem_encontrou"] = row.get("quem_encontrou_username")
            row_data["dono"] = row.get("dono_username")
            
            item = Item(data=row_data)
            itens.append(item)

        return itens


    def get_itens_by_instituicao_by_categoria(cnpj, codigo_categoria):
        from main import supabase
        from models.item import Item

        response = supabase.table('itens').select("*").eq("instituicao_cnpj", cnpj).eq("categoria_codigo", codigo_categoria).execute()
        itens = []

        data_rows = response.data if hasattr(response, 'data') else response

        for row in data_rows:
            # Mapeia as colunas do banco para as chaves limpas que a classe Item espera
            row_data = row.copy()
            row_data["categoria"] = row.get("categoria_codigo")
            row_data["instituicao"] = row.get("instituicao_cnpj")
            row_data["onde_guardado"] = row.get("onde_guardado_codigo")
            row_data["quem_encontrou"] = row.get("quem_encontrou_username")
            row_data["dono"] = row.get("dono_username")
            
            item = Item(data=row_data)
            itens.append(item)

        return itens        

    def add_item(self, item):
        from main import supabase
        
        dados = {
            "codigo": item.codigo,
            "cor": item.cor,
            "tamanho": item.tamanho,
            "material": item.material,
            "detalhes": item.detalhes,
            "foto": item.foto,
            "status": int(item.status),
            "data_cadastro": str(item.data_cadastro),
            "data_devolucao": str(item.data_devolucao) if item.data_devolucao else None,
            "onde_encontrado": item.onde_encontrado,
            "categoria_codigo": item.categoria,
            "instituicao_cnpj": item.instituicao,
            "onde_guardado_codigo": item.onde_guardado,
            "quem_encontrou_username": item.quem_encontrou,
            "dono_username": item.dono
        }
        
        try:
            resposta = supabase.table("itens").insert(dados).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao adicionar item: {erro}")
            return None

    def get_item_by_codigo(self, codigo):
        from main import supabase
        from models.item import Item
        
        try:
            resposta = supabase.table("itens").select("*").eq("codigo", codigo).execute()
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta
            
            if data_rows and len(data_rows) > 0:
                row = data_rows[0]
                row_data = row.copy()
                row_data["categoria"] = row.get("categoria_codigo")
                row_data["instituicao"] = row.get("instituicao_cnpj")
                row_data["onde_guardado"] = row.get("onde_guardado_codigo")
                row_data["quem_encontrou"] = row.get("quem_encontrou_username")
                row_data["dono"] = row.get("dono_username")
                return Item(data=row_data)
        except Exception as erro:
            print(f"Erro ao buscar item por código: {erro}")
            
        return None

    def atualizar_item(self, item):
        from main import supabase
        
        dados = {
            "cor": item.cor,
            "tamanho": item.tamanho,
            "material": item.material,
            "detalhes": item.detalhes,
            "foto": item.foto,
            "status": int(item.status),
            "data_devolucao": str(item.data_devolucao) if item.data_devolucao else None,
            "onde_encontrado": item.onde_encontrado,
            "categoria_codigo": item.categoria,
            "instituicao_cnpj": item.instituicao,
            "onde_guardado_codigo": item.onde_guardado,
            "quem_encontrou_username": item.quem_encontrou,
            "dono_username": item.dono
        }
        
        try:
            resposta = supabase.table("itens").update(dados).eq("codigo", item.codigo).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao atualizar item: {erro}")
            return None

    def deletar_item(self, codigo):
        from main import supabase
        
        try:
            resposta = supabase.table("itens").delete().eq("codigo", codigo).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao deletar item: {erro}")
            return None

    def contar_total(self):
        from main import supabase
        try:
            resposta = supabase.table("itens").select("*", count="exact", head=True).execute()
            return resposta.count if resposta.count is not None else 0
        except Exception as e:
            print(f"Erro ao contar total de itens: {e}")
            return 0