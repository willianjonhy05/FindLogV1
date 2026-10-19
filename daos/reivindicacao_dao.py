class ReivindicacaoDAO:

    def buscar_reivincacao_por_protocolo(self, protocolo):
        from main import supabase
        from models.reivindicacao import Reivindicacao

        response = supabase.table('reivindicacoes').select("*").eq("protocolo", protocolo).execute()
        data_rows = response.data if hasattr(response, 'data') else response

        if data_rows and len(data_rows) > 0:
            return Reivindicacao(data=data_rows[0])
        return None

    def contar_total():
        from main import supabase

        response = supabase.table("reivindicacoes").select("*", count="exact").execute()
        return response.count if hasattr(response, 'count') else len(response.data)


    def get_reivindicacoes(self):
        from main import supabase
        from models.reivindicacao import Reivindicacao

        response = supabase.table('reivindicacoes').select("*").execute()
        reivindicacoes = []

        data_rows = response.data if hasattr(response, 'data') else response
        
        for row in data_rows:
            # Passamos o dicionário row diretamente para o construtor da Instituição
            reivindicacao = Reivindicacao(data=row)
            reivindicacoes.append(reivindicacao)
        return reivindicacoes

    def get_reivindicacoes_por_item(self, codigo_item):
        from main import supabase
        from models.reivindicacao import Reivindicacao

        try:
            response = supabase.table('reivindicacoes').select("*").eq("item_codigo", codigo_item).execute()
            reivindicacoes = []

            # Garante que data_rows receba os dados corretamente
            data_rows = response.data if hasattr(response, 'data') else response
            
            # Previne erro de iteração caso a consulta não retorne nada (None)
            if not data_rows:
                return []
            
            for row in data_rows:
                # Passamos o dicionário row diretamente para o construtor da Reivindicacao
                reivindicacao = Reivindicacao(data=row)
                reivindicacoes.append(reivindicacao)
                
            return reivindicacoes

        except Exception as erro:
            print(f"Erro ao buscar reivindicações para o item {codigo_item}: {repr(erro)}")
            return []  # Retorna lista vazia em caso de falha para não quebrar a aplicação


    def inserir(self, reivindicacao):
        from main import supabase

        # Mapeando os dados do objeto Reivindicacao para o formato do banco
        dados = {
            "protocolo": reivindicacao.protocolo,
            "autor": reivindicacao.autor,
            "item_codigo": reivindicacao.item_codigo,
            "instituicao_cnpj": reivindicacao.instituicao_cnpj,
            "descricao": reivindicacao.descricao,
            "prova_propriedade": reivindicacao.prova_propriedade,
            "status": reivindicacao.status,
            "observacoes_admin": reivindicacao.observacoes_admin,
            "anexos": reivindicacao.anexos,
            "responsavel_id": reivindicacao.responsavel_id,
            "local_devolucao": reivindicacao.local_devolucao,
            "data_devolucao": reivindicacao.data_devolucao,
            "data_criacao": reivindicacao.data_criacao
        }

        # Remove chaves com valores None para que o banco aplique os valores default se necessário
        dados_limpos = {k: v for k, v in dados.items() if v is not None}

        try:
            resposta = (
                supabase.table("reivindicacoes")
                .insert(dados_limpos)
                .select("*")
                .execute()
            )
            
            return resposta.data[0] if resposta.data else None

        except Exception as erro:
            print(f"Erro ao salvar reivindicação no Supabase: {repr(erro)}")
            raise    



