from database.sqlitedb import SQLiteDB


class SalaDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def get_salas(self):
        from main import supabase
        from models.sala import Sala
        response = supabase.table('salas').select("*").execute()
        salas = []
        for row in response.data:
            sala = Sala(
                telefone=row["telefone"],
                andar=row["andar"],
                numero=row["numero"],
                descricao=row["descricao"],
                predio=row["predio"],
                instituicao=self.nome_por_cnpj(row["instituicao_cnpj"]),
                laboratorio=bool(row["laboratorio"]),
                sala_de_aula=bool(row["sala_de_aula"]),
                codigo=row["codigo"]
            )
            salas.append(sala)
        return salas
    
    def add_sala(self, sala):
        from main import supabase
        
        dados = {
            "telefone": sala.telefone,
            "andar": sala.andar,
            "numero": sala.numero,
            "descricao": sala.descricao,
            "predio": sala.predio,
            "instituicao_cnpj": sala.instituicao.cnpj,
            "laboratorio": int(sala.laboratorio),
            "sala_de_aula": int(sala.sala_de_aula),
            "codigo": sala.codigo
        }
        
        resposta = supabase.table("salas").insert(dados).execute()
        return resposta.data[0] if resposta.data else None
 