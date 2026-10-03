
from database.sqlitedb import SQLiteDB


class InstituicaoDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def get_instituicoes(self):
        from main import supabase
        from models.instituicao import Instituicao
        response = supabase.table('instituicoes').select("*").execute()
        instituicoes = []
        for row in response.data:
            instituicao = Instituicao(
                nome=row["nome"],
                cnpj=row["cnpj"],
                endereco=row["endereco"],
                telefone=row["telefone"],
                email=row["email"]
            )
            instituicao.ativo = bool(row["ativo"])
            instituicoes.append(instituicao)
        return instituicoes
        
        
        # self.db.conectar()
        # sql = "SELECT nome, cnpj, endereco, telefone, email, ativo FROM instituicoes;"
        # resultados = self.db.consultar(query=sql)
        # instituicoes = []
        # for row in resultados:
        #     nome=row[0]
        #     cnpj=row[1]
        #     endereco=row[2]
        #     telefone=row[3]
        #     email=row[4]
        #     instituicao = Instituicao(nome=nome, cnpj=cnpj, endereco=endereco, telefone=telefone, email=email)
        #     instituicao.ativo = bool(row[5])
        #     instituicoes.append(instituicao)
        # self.db.desconectar()
        # return instituicoes

    from models.instituicao import Instituicao
    def add_instituicao(self, instituicao):
        from main import supabase
        
        dados = {
            "nome": instituicao.nome,
            "cnpj": instituicao.cnpj,
            "endereco": instituicao.endereco,
            "telefone": instituicao.telefone,
            "email": instituicao.email,
            "ativo": int(instituicao.ativo)
        }
        
        resposta = supabase.table("instituicoes").insert(dados).execute()
        return resposta.data[0] if resposta.data else None

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
        resposta = supabase.table("instituicoes").delete().eq("cnpj", cnpj).execute()
        return resposta.data[0] if resposta.data else None
        # self.db.conectar()
        # sql = "DELETE FROM instituicoes WHERE cnpj = ?;"
        # self.db.executar(sql, (cnpj,))
        # self.db.desconectar()
        
        
    def atualizar_instituicao(self, instituicao):
        from main import supabase
        dados = {
            "nome": instituicao.nome,
            "cnpj": instituicao.cnpj,
            "endereco": instituicao.endereco,
            "telefone": instituicao.telefone,
            "email": instituicao.email,
            "ativo": int(instituicao.ativo)
        }
        resposta = supabase.table("instituicoes").update(dados).eq("cnpj", instituicao.cnpj).execute()
        return resposta.data[0] if resposta.data else None
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
        instituicao = supabase.table("instituicoes").select("*").eq("cnpj", cnpj).execute()
        if instituicao.data:
            row = instituicao.data[0]
            instituicao = Instituicao(
                nome=row["nome"],
                cnpj=row["cnpj"],
                endereco=row["endereco"],
                telefone=row["telefone"],
                email=row["email"]
            )
            instituicao.ativo = bool(row["ativo"])
            return instituicao
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
        response = supabase.table("instituicoes").select("nome, cnpj, ativo").execute()
        instituicoes = []
        for row in response.data:
            if row["ativo"]:
                instituicao = Instituicao(
                    nome=row["nome"],
                    cnpj=row["cnpj"]
            )
            instituicoes.append(instituicao)
        return instituicoes
    
    
    def get_nome_por_cnpj(self, cnpj):
        from main import supabase
        response = supabase.table("instituicoes").select("nome").eq("cnpj", cnpj).execute()
        if response.data:
            return response.data[0]["nome"]
        return None
    
