
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

