from models.usuario import Usuario
from models.item import Item
from models.instituicao import Instituicao
from datetime import datetime
import random
from daos.reivindicacao_dao import ReivindicacaoDAO

class Reivindicacao():
    STATUS = {
        1: "Pendente",
        2: "Em Análise",
        3: "Aprovada",
        4: "Recusada",
        5: "Entregue"
    }

    def __init__(self, data=None):
        self.data = data or {}
        self.errors = []

        # Data da reivindicação preenchida automaticamente se não existir
        if not self.data.get("data"):
            self.data["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   

        if not self.data.get("protocolo"):
            self.data["protocolo"] = self._gerar_id()

        if not self.data.get("status"):
            self.data["status"] = self.STATUS[1] # Pendente         




    def validate(self, is_new=True):
        self.errors = []

        autor = self.data.get("autor")
        if autor and not Usuario.get_by_username(autor):
            self.errors.append("O autor da reivindicação não existe")  

        item_codigo = self.data.get["item_codigo"]  
        if item_codigo and not Item.get_by_codigo(item_codigo):
            self.errors.append("O item da reivindicação não existe")

        instituicao_cnpj = self.data.get("instituicao")
        if not instituicao_cnpj:
            self.errors.append("A instituição é obrigatória.")
        else:
            inst = Instituicao.get_by_cnpj(instituicao_cnpj)
            if not inst:
                self.errors.append("A instituição selecionada não existe.")   

        prova_propriedade = self.data.get("prova_propriedade")        
        if len(prova_propriedade) < 10:
            self.errors.append("Descrição insuficiente")


        return len(self.errors) == 0


    @classmethod
    def _gerar_protocolo(cls):
        while True:
            protocolo = random.randint(1000000, 9999999)
            if not cls.pegar_por_protocolo(protocolo):
                return protocolo 

    @staticmethod
    def pegar_por_protocolo(protocolo):
        dao = ReivindicacaoDAO()
        return dao.buscar_reivincacao_por_protocolo(protocolo)


    @property
    def protocolo(self):
        return self.data.get("protocolo")

    @property
    def item_codigo(self):
        return self.data.get("item_codigo")

    @property
    def autor(self):
        return self.data.get("autor")

    @property
    def instituicao_cnpj(self):
        return self.data.get("instituicao_cnpj")

    @property
    def descricao(self):
        return self.data.get("descricao")
        
    @property
    def prova_propriedade(self):
        return self.data.get("prova_propriedade")

    @property
    def status(self):
        return self.data.get("status")

    @property
    def observacoes_admin(self):
        return self.data.get("observacoes_admin")    

    @property
    def anexos(self):
        return self.data.get("anexos")

    @property
    def responsavel_id(self):
        return self.data.get("responsavel_id")

    @property
    def local_devolucao(self):
        return self.data.get("local_devolucao")
