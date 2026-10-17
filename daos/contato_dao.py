
class ContatoDAO:


    def inserir(self, contato):
        from main import supabase

        dados = {
            "codigo": contato.codigo,
            "nome": contato.nome,
            "email": contato.email,
            "telefone": contato.telefone,
            "assunto": contato.assunto,
            "mensagem": contato.mensagem,
            "data_envio": contato.data_envio
        }

        try:
            print("Dados enviados ao Supabase:", dados)

            resposta = (
                supabase.table("contatos")
                .insert(dados)
                .select("*")
                .execute()
            )

            print("Resposta do Supabase:", resposta.data)

            if resposta.data:
                return resposta.data[0]

            print("O Supabase não retornou o registro inserido.")
            return None

        except Exception as erro:
            print("ERRO AO SALVAR CONTATO:", repr(erro))
            raise


    def listar_todos(self):
        from main import supabase
        from models.contato import Contato

        try:
            resposta = (
                supabase.table("contatos")
                .select("*")
                .order("data_envio", desc=True)
                .execute()
            )

            data_rows = resposta.data if hasattr(resposta, 'data') else resposta

            contatos = []

            for row in data_rows:
                contato = Contato(data=row)
                contatos.append(contato)

            return contatos

        except Exception as erro:
            print(f"Erro ao listar mensagens: {erro}")
            return []

    def buscar_por_codigo(self, codigo):
        from main import supabase
        from models.contato import Contato

        try:
            resposta = (
                supabase.table("contatos")
                .select("*")
                .eq("codigo", codigo)
                .execute()
            )
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta
            if data_rows and len(data_rows) > 0:
                return Contato(data=data_rows[0])

        except Exception as erro:
            print(f"Erro ao buscar mensagem: {erro}")
            return None

    def deletar(self, codigo):
        from main import supabase

        try:
            resposta = (
                supabase.table("contatos")
                .delete()
                .eq("codigo", codigo)
                .execute()
            )

            return resposta.data[0] if resposta.data else None

        except Exception as erro:
            print(f"Erro ao excluir mensagem: {erro}")
            return None


    def contar_total(self):
        from main import supabase
        try:
            resposta = supabase.table("contatos").select("*", count="exact", head=True).execute()
            return resposta.count if resposta.count is not None else 0
        except Exception as e:
            print(f"Erro ao contar total de contatos: {e}")
            return 0