
from database.sqlitedb import SQLiteDB


class InstituicaoDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def get_instituicoes(self):
        from models.instituicao import Instituicao
        self.db.conectar()
        sql = "SELECT nome, cnpj, endereco, telefone, email, ativo FROM instituicoes;"
        resultados = self.db.consultar(query=sql)
        instituicoes = []
        for row in resultados:
            nome=row[0]
            cnpj=row[1]
            endereco=row[2]
            telefone=row[3]
            email=row[4]
            instituicao = Instituicao(nome=nome, cnpj=cnpj, endereco=endereco, telefone=telefone, email=email)
            instituicao.ativo = bool(row[5])
            instituicoes.append(instituicao)
        self.db.desconectar()
        return instituicoes

    from models.instituicao import Instituicao
    def add_instituicao(self, instituicao):

        self.db.conectar()

        sql = """
        INSERT INTO instituicoes 
        (nome, cnpj, endereco, telefone, email, ativo)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        self.db.executar(
            sql,
            (
                instituicao.nome,
                instituicao.cnpj,
                instituicao.endereco,
                instituicao.telefone,
                instituicao.email,
                int(instituicao.ativo)
            )
        )

        self.db.desconectar()

        return 1  


    def deletar_instituicao(self, cnpj):
        self.db.conectar()
        sql = "DELETE FROM instituicoes WHERE cnpj = ?;"
        self.db.executar(sql, (cnpj,))
        self.db.desconectar()
        
    def atualizar_instituicao(self, instituicao):
        self.db.conectar()
        sql = """
        UPDATE instituicoes
        SET nome = ?, endereco = ?, telefone = ?, email = ?, ativo = ?
        WHERE cnpj = ?;
        """
        self.db.executar(
            sql,
            (
                instituicao.nome,
                instituicao.endereco,
                instituicao.telefone,
                instituicao.email,
                int(instituicao.ativo),
                instituicao.cnpj
            )
        )
        self.db.desconectar()
        
        
    def get_instituicao_by_cnpj(self, cnpj):
        from models.instituicao import Instituicao
        self.db.conectar()
        sql = "SELECT nome, cnpj, endereco, telefone, email, ativo FROM instituicoes WHERE cnpj = ?;"
        resultado = self.db.consultar(query=sql, params=(cnpj,))
        self.db.desconectar()
        if resultado:
            row = resultado[0]
            instituicao = Instituicao(nome=row[0], cnpj=row[1], endereco=row[2], telefone=row[3], email=row[4])
            instituicao.ativo = bool(row[5])
            return instituicao
        return None
