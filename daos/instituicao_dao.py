

class InstituicaoDAO:
    def __init__(self):
        pass

    def get_instituicoes(self):
        from main import supabase
        from models.instituicao import Instituicao
        """Retorna uma lista com todas as instituições cadastradas."""
        response = supabase.table('instituicoes').select("*").execute()
        instituicoes = []
        
        data_rows = response.data if hasattr(response, 'data') else response
        
        for row in data_rows:
            # Passamos o dicionário row diretamente para o construtor da Instituição
            instituicao = Instituicao(data=row)
            instituicoes.append(instituicao)
        return instituicoes

    def get_instituicoes_paginated(self, page=1, per_page=10, search=None):
        from main import supabase
        from models.instituicao import Instituicao
        
        # Calcula o intervalo para paginação
        start = (page - 1) * per_page
        end = start + per_page - 1
        
        # Inicia a query básica pedindo contagem exata
        query = supabase.table('instituicoes').select("*", count="exact")
        
        # Se houver um termo de pesquisa, aplica o filtro OR (nome ou cnpj)
        if search and search.strip():
            termo = f"%{search.strip()}%"
            # O .or_() no Supabase Python filtra se o termo bate em qualquer um dos campos
            query = query.or_(f"nome.ilike.{termo},cnpj.ilike.{termo}")
            
        # Aplica a ordenação e a paginação por range
        response = query.range(start, end).execute()
            
        instituicoes = []
        data_rows = response.data if hasattr(response, 'data') else []
        
        for row in data_rows:
            instituicao = Instituicao(data=row)
            instituicoes.append(instituicao)
            
        total_count = response.count if hasattr(response, 'count') else len(data_rows)
        
        return instituicoes, total_count

    
    from models.instituicao import Instituicao
    def add_instituicao(self, instituicao):
        from main import supabase
        """Insere uma nova instituição no banco."""
        dados = {
            "nome": instituicao.nome,
            "cnpj": instituicao.cnpj,
            "endereco": instituicao.endereco,
            "telefone": instituicao.telefone,
            "email": instituicao.email,
            "ativo": bool(instituicao.ativo)
        }
        
        resposta = supabase.table("instituicoes").insert(dados).execute()
        data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
        return data_resposta[0] if data_resposta else None

        
        # dados = {
        #     "nome": instituicao.nome,
        #     "cnpj": instituicao.cnpj,
        #     "endereco": instituicao.endereco,
        #     "telefone": instituicao.telefone,
        #     "email": instituicao.email,
        #     "ativo": int(instituicao.ativo)
        # }
        
        # resposta = supabase.table("instituicoes").insert(dados).execute()
        # return resposta.data[0] if resposta.data else None

        # self.db.conectar()

        # sql = """
        # INSERT INTO instituicoes 
        # (nome, cnpj, endereco, telefone, email, ativo)
        # VALUES (?, ?, ?, ?, ?, ?)
        # """

        # self.db.executar(
        #     sql,
        #     (
        #         instituicao.nome,
        #         instituicao.cnpj,
        #         instituicao.endereco,
        #         instituicao.telefone,
        #         instituicao.email,
        #         int(instituicao.ativo)
        #     )
        # )

        # self.db.desconectar()

        return 1  


    def deletar_instituicao(self, cnpj):
        from main import supabase
        """Remove uma instituição do banco pelo CNPJ."""
        resposta = supabase.table("instituicoes").delete().eq("cnpj", cnpj).execute()
        return resposta
    
        # resposta = supabase.table("instituicoes").delete().eq("cnpj", cnpj).execute()
        # return resposta.data[0] if resposta.data else None
    


        # self.db.conectar()
        # sql = "DELETE FROM instituicoes WHERE cnpj = ?;"
        # self.db.executar(sql, (cnpj,))
        # self.db.desconectar()
        
        
    def atualizar_instituicao(self, instituicao):
        from main import supabase
        
        """Atualiza os dados de uma instituição existente com base no CNPJ."""
        dados = {
            "nome": instituicao.nome,
            "endereco": instituicao.endereco,
            "telefone": instituicao.telefone,
            "email": instituicao.email,
            "ativo": bool(instituicao.ativo)
        }
        
        resposta = supabase.table("instituicoes").update(dados).eq("cnpj", instituicao.cnpj).execute()
        data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
        return data_resposta[0] if data_resposta else None


    def quantidade_instituicoes():
        from main import supabase
        # Faz a consulta pedindo apenas a contagem exata
        response = supabase.table("instituicoes").select("*", count="exact").execute()
        
        # O número total de registros vem na propriedade 'count' do objeto de resposta
        return response.count if hasattr(response, 'count') else len(response.data)
        
        # dados = {
        #     "nome": instituicao.nome,
        #     "cnpj": instituicao.cnpj,
        #     "endereco": instituicao.endereco,
        #     "telefone": instituicao.telefone,
        #     "email": instituicao.email,
        #     "ativo": int(instituicao.ativo)
        # }
        # resposta = supabase.table("instituicoes").update(dados).eq("cnpj", instituicao.cnpj).execute()
        # return resposta.data[0] if resposta.data else None
    


        # self.db.conectar()
        # sql = """
        # UPDATE instituicoes
        # SET nome = ?, endereco = ?, telefone = ?, email = ?, ativo = ?
        # WHERE cnpj = ?;
        # """
        # self.db.executar(
        #     sql,
        #     (
        #         instituicao.nome,
        #         instituicao.endereco,
        #         instituicao.telefone,
        #         instituicao.email,
        #         int(instituicao.ativo),
        #         instituicao.cnpj
        #     )
        # )
        # self.db.desconectar()
        
        
    def get_instituicao_by_cnpj(self, cnpj):
        from main import supabase
        from models.instituicao import Instituicao

        """Busca uma instituição específica pelo CNPJ."""
        response = supabase.table('instituicoes').select("*").eq("cnpj", cnpj).execute()
        data_rows = response.data if hasattr(response, 'data') else response
        
        if data_rows and len(data_rows) > 0:
            return Instituicao(data=data_rows[0])
        return None


        # instituicao = supabase.table("instituicoes").select("*").eq("cnpj", cnpj).execute()
        # if instituicao.data:
        #     row = instituicao.data[0]
        #     instituicao = Instituicao(
        #         nome=row["nome"],
        #         cnpj=row["cnpj"],
        #         endereco=row["endereco"],
        #         telefone=row["telefone"],
        #         email=row["email"]
        #     )
        #     instituicao.ativo = bool(row["ativo"])
        #     return instituicao

        
        # from models.instituicao import Instituicao
        # self.db.conectar()
        # sql = "SELECT nome, cnpj, endereco, telefone, email, ativo FROM instituicoes WHERE cnpj = ?;"
        # resultado = self.db.consultar(query=sql, params=(cnpj,))
        # self.db.desconectar()
        # if resultado:
        #     row = resultado[0]
        #     instituicao = Instituicao(nome=row[0], cnpj=row[1], endereco=row[2], telefone=row[3], email=row[4])
        #     instituicao.ativo = bool(row[5])
        #     return instituicao
        # return None
        
        
    def get_nome_e_cnpj_ativos(self):
        from main import supabase
        from models.instituicao import Instituicao

        """Retorna apenas o nome e CNPJ das instituições ativas."""
        response = supabase.table('instituicoes').select("nome, cnpj").eq("ativo", True).execute()
        return response.data if hasattr(response, 'data') else response

        # response = supabase.table("instituicoes").select("nome, cnpj, ativo").execute()
        # instituicoes = []
        # for row in response.data:
        #     if row["ativo"]:
        #         instituicao = Instituicao(
        #             nome=row["nome"],
        #             cnpj=row["cnpj"]
        #     )
        #     instituicoes.append(instituicao)
        # return instituicoes
    
    
    def get_nome_por_cnpj(self, cnpj):
        from main import supabase

        """Retorna o nome de uma instituição dado o seu CNPJ."""
        response = supabase.table('instituicoes').select("nome").eq("cnpj", cnpj).execute()
        data_rows = response.data if hasattr(response, 'data') else response
        if data_rows and len(data_rows) > 0:
            return data_rows[0].get("nome")
        return None


        # response = supabase.table("instituicoes").select("nome").eq("cnpj", cnpj).execute()
        # if response.data:
        #     return response.data[0]["nome"]
        # return None


    def desativar_instituicao(self, instituicao):
        from main import supabase

        dados = {
            "ativo": bool(instituicao.ativo)
        }

        response = supabase.table('instituicoes').update(dados). eq("cnpj", instituicao.cnpj).execute()

        data_resposta = response.data if hasattr(response, 'data') else response
        return data_resposta[0] if data_resposta else None
    
