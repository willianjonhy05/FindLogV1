from database import supabase


class ContatoDAO:

    def inserir(self, contato):
        resposta = (
            supabase.table("contatos")
            .insert({
                "nome": contato.nome,
                "email": contato.email,
                "telefone": contato.telefone,
                "assunto": contato.assunto,
                "mensagem": contato.mensagem
            })
            .select("*")
            .execute()
        )

        if resposta.data:
            return resposta.data[0]

        return None

    def listar_todos(self):
        resposta = (
            supabase.table("contatos")
            .select("*")
            .order("data_envio", desc=True)
            .execute()
        )

        return resposta.data or []

    def buscar_por_id(self, id):
        resposta = (
            supabase.table("contatos")
            .select("*")
            .eq("id", id)
            .execute()
        )

        if resposta.data:
            return resposta.data[0]

        return None

    def deletar(self, id):
        resposta = (
            supabase.table("contatos")
            .delete()
            .eq("id", id)
            .execute()
        )

        if resposta.data:
            return resposta.data[0]

        return None

    
    def atualizar(self, id, contato):
        resposta = (
            supabase.table("contatos")
            .update({
                "nome": contato.nome,
                "email": contato.email,
                "telefone": contato.telefone,
                "assunto": contato.assunto,
                "mensagem": contato.mensagem
            })
            .eq("id", id)
            .execute()
        )

        if resposta.data:
            return resposta.data[0]

        return None
