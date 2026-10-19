from models.usuario import Usuario
from models.item import Item
from models.instituicao import Instituicao
from datetime import datetime
import random
from daos.reivindicacao_dao import ReivindicacaoDAO

class Reivindicacao:
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
        if not self.data.get("data_criacao"):
            self.data["data_criacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   

        # Correção: chamando o classmethod corretamente pelo nome certo
        if not self.data.get("protocolo"):
            self.data["protocolo"] = Reivindicacao._gerar_protocolo()

        if not self.data.get("status"):
            self.data["status"] = self.STATUS[1] # Pendente        

    def validate(self, is_new=True):
        self.errors = []

        autor = self.data.get("autor")
        if not autor or not Usuario.get_by_username(autor):
            self.errors.append("O autor da reivindicação não existe ou não foi informado.")  

        # Correção: 'get' é um método, exige parênteses e não colchetes
        item_codigo = self.data.get("item_codigo")  
        if not item_codigo or not Item.get_by_codigo(item_codigo):
            self.errors.append("O item da reivindicação não existe ou não foi informado.")

        # Correção: padronizado para a mesma chave da property (instituicao_cnpj)
        instituicao_cnpj = self.data.get("instituicao_cnpj")
        if not instituicao_cnpj:
            self.errors.append("A instituição é obrigatória.")
        else:
            inst = Instituicao.get_by_cnpj(instituicao_cnpj)
            if not inst:
                self.errors.append("A instituição selecionada não existe.")   

        prova_propriedade = self.data.get("prova_propriedade")        
        # Correção: garantindo que a prova seja uma string antes de medir o tamanho (evita erro se for None)
        if not prova_propriedade or len(str(prova_propriedade).strip()) < 10:
            self.errors.append("Descrição da prova de propriedade insuficiente.")

        return len(self.errors) == 0


    def save(self):
        dao = ReivindicacaoDAO
        return dao.inserir(self)

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

    @staticmethod
    def get_all():        
        dao = ReivindicacaoDAO()
        return dao.get_reivindicacoes()

    @staticmethod
    def quantidade_de_revindicacoes():
        dao = ReivindicacaoDAO()
        return dao.contar_total()    

    @staticmethod
    def get_by_item(codigo):
        dao = ReivindicacaoDAO()
        return dao.get_reivindicacoes_por_item(codigo)

    @property
    def protocolo(self):
        return self.data.get("protocolo")
        
    @property
    def data_criacao(self):
        return self.data.get("data_criacao")

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

    @property
    def data_devolucao(self):
        return self.data.get("data_devolucao")

    @property
    def item_obj(self):
        """Busca o objeto Item completo no banco de dados baseado no item_codigo"""
        if not self.item_codigo:
            return None
        from models.item import Item
        return Item.get_by_codigo(self.item_codigo)    

    @property
    def autor_obj(self):
        """Busca o objeto Usuario completo no banco de dados baseado no username (autor)"""
        if not self.autor:
            return None
        from models.usuario import Usuario
        return Usuario.get_by_username(self.autor)    