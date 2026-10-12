class SalaDAO:

    def get_salas(self):
        from main import supabase
        from models.sala import Sala
        
        response = supabase.table('salas').select("*").execute()
        salas = []
        
        data_rows = response.data if hasattr(response, 'data') else response
        
        for row in data_rows:
            # Fazemos uma cópia para mapear a coluna do banco 'instituicao_cnpj' 
            # para a chave 'instituicao' que a classe Sala utiliza internamente.
            row_data = row.copy()
            row_data["instituicao"] = row.get("instituicao_cnpj")
            
            sala = Sala(data=row_data)
            salas.append(sala)
            
        return salas
    
    def add_sala(self, sala):
        from main import supabase
        
        dados = {
            "codigo": sala.codigo,
            "telefone": sala.telefone,
            "andar": sala.andar,
            "numero": sala.numero,
            "descricao": sala.descricao,
            "predio": sala.predio,
            "instituicao_cnpj": sala.instituicao, # sala.instituicao já armazena o CNPJ
            "laboratorio": bool(sala.laboratorio),
            "sala_de_aula": bool(sala.sala_de_aula)
        }
        
        try:
            resposta = supabase.table("salas").insert(dados).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao adicionar sala: {erro}")
            return None

    def get_sala_by_codigo(self, codigo):
        from main import supabase
        from models.sala import Sala
        
        try:
            resposta = supabase.table("salas").select("*").eq("codigo", codigo).execute()
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta
            
            if data_rows and len(data_rows) > 0:
                row = data_rows[0]
                row_data = row.copy()
                row_data["instituicao"] = row.get("instituicao_cnpj")
                return Sala(data=row_data)
        except Exception as erro:
            print(f"Erro ao buscar sala por código: {erro}")
            
        return None

    def atualizar_sala(self, sala):
        from main import supabase
        
        dados = {
            "telefone": sala.telefone,
            "andar": sala.andar,
            "numero": sala.numero,
            "descricao": sala.descricao,
            "predio": sala.predio,
            "instituicao_cnpj": sala.instituicao,
            "laboratorio": bool(sala.laboratorio),
            "sala_de_aula": bool(sala.sala_de_aula)
        }
        
        try:
            resposta = supabase.table("salas").update(dados).eq("codigo", sala.codigo).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao atualizar sala: {erro}")
            return None

    def deletar_sala(self, codigo):
        from main import supabase
        
        try:
            resposta = supabase.table("salas").delete().eq("codigo", codigo).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao deletar sala: {erro}")
            return None

    def contar_total(self):
        from main import supabase
        try:
            resposta = supabase.table("salas").select("*", count="exact", head=True).execute()
            return resposta.count if resposta.count is not None else 0
        except Exception as e:
            print(f"Erro ao contar total de salas: {e}")
            return 0