
class ContatoDAO:


    def inserir(self, contato):
        from main import supabase

        dados = {
            "codigo": contato.codigo,
            "nome": contato.nome,
            "email": contato.email,
            "telefone": contato.telefone,
            "assunto": contato.assunto,
            "mensagem": contato.mensagem
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

        try:
            resposta = (
                supabase.table("contatos")
                .select("*")
                .order("data_envio", desc=True)
                .execute()
            )

            return resposta.data or []

        except Exception as erro:
            print(f"Erro ao listar mensagens: {erro}")
            return []

    def buscar_por_codigo(self, codigo):
        from main import supabase

        try:
            resposta = (
                supabase.table("contatos")
                .select("*")
                .eq("codigo", codigo)
                .execute()
            )

            return resposta.data[0] if resposta.data else None

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
