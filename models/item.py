from datetime import datetime
import random
import string
from models.categoria import Categoria
from models.instituicao import Instituicao
from models.usuario import Usuario
from models.sala import Sala

class Item:
    TIPOS_STATUS = {
        1: "Perdido",
        2: "Encontrado",
        3: "Guardado",
        4: "Devolvido",
        5: "Aguardando devolução"
    }

    def __init__(self, data=None):
        self.data = data or {}
        self.errors = []

        # Status padrão: 1 (Perdido) se não informado
        if "status" not in self.data:
            self.data["status"] = 1

        # Data de cadastro preenchida automaticamente se não existir
        if not self.data.get("data_cadastro"):
            self.data["data_cadastro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Código único e imutável gerado automaticamente se não existir
        if not self.data.get("codigo"):
            self.data["codigo"] = self._gerar_codigo_unico()

    def __str__(self):
        cor = self.data.get("cor", "Item")
        material = self.data.get("material", "")
        return f"{cor} {material}".strip() or f"Item {self.codigo}"

    def validate(self, is_new=True):
        self.errors = []

        # Cor (Obrigatório)
        if not self.data.get("cor") or not str(self.data["cor"]).strip():
            self.errors.append("A cor do item não pode ser vazia.")

        # Status (Obrigatório e Válido)
        status = self.data.get("status")
        if status not in self.TIPOS_STATUS:
            self.errors.append("O status do item é inválido.")

        # Categoria (Obrigatório e deve existir)
        cat_codigo = self.data.get("categoria")
        if not cat_codigo:
            self.errors.append("A categoria do item é obrigatória.")
        else:
            if not Categoria.get_by_codigo(cat_codigo):
                self.errors.append("A categoria informada não existe.")

        # Instituição (Obrigatório e deve existir)
        inst_cnpj = self.data.get("instituicao")
        if not inst_cnpj:
            self.errors.append("A instituição é obrigatória.")
        else:
            if not Instituicao.get_by_cnpj(inst_cnpj):
                self.errors.append("A instituição informada não existe.")

        # Regra de Onde Guardado: Obrigatório se o status for 3 (Guardado)
        onde_guardado = self.data.get("onde_guardado")
        if status == 3 and not onde_guardado:
            self.errors.append("O local onde está guardado (Sala) é obrigatório para itens com status 'Guardado'.")
        elif onde_guardado:
            if not Sala.get_by_codigo(onde_guardado):
                self.errors.append("A sala informada onde o item está guardado não existe.")

        # Quem Encontrou (Opcional, mas validado se preenchido)
        quem_encontrou = self.data.get("quem_encontrou")
        if quem_encontrou and not Usuario.get_by_username(quem_encontrou):
            self.errors.append("O usuário registrado como 'quem encontrou' não existe.")

        # Dono (Opcional, mas validado se preenchido)
        dono = self.data.get("dono")
        if dono and not Usuario.get_by_username(dono):
            self.errors.append("O usuário registrado como 'dono' não existe.")

        # Unicidade do Código (Apenas para novos cadastros)
        if is_new:
            codigo = self.data.get("codigo")
            if codigo and Item.get_by_codigo(codigo):
                self.errors.append("Já existe um item cadastrado com este código.")

        return len(self.errors) == 0

    @classmethod
    def _gerar_codigo_unico(cls):
        """Gera um código alfanumérico único para o item (ex: IT-A8F2)"""
        while True:
            sufixo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            codigo = f"IT-{sufixo}"
            if not cls.get_by_codigo(codigo):
                return codigo

    @staticmethod
    def contar_total():
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.contar_total()


    def save(self):
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.add_item(self)

    def update(self):
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.atualizar_item(self)

    def delete(self):
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.deletar_item(self.codigo)

    @staticmethod
    def get_all():
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.get_itens()

    @staticmethod
    def get_all_instituicao(cnpj):
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.get_itens_by_instituicao(cnpj)

    @staticmethod
    def get_all_instituicao_by_categoria(cnpj, codigo_categoria):
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.get_itens_by_instituicao_by_categoria(cnpj, codigo_categoria)

    @staticmethod
    def get_by_codigo(codigo):
        from daos.item_dao import ItemDAO
        dao = ItemDAO()
        return dao.get_item_by_codigo(codigo)

    # ==========================
    # PROPRIEDADES (Getters e Setters)
    # ==========================

    @property
    def codigo(self):
        return self.data.get("codigo")  # Imutável

    @property
    def cor(self):
        return self.data.get("cor")

    @cor.setter
    def cor(self, value):
        if not value or not str(value).strip():
            raise ValueError("A cor não pode ser vazia.")
        self.data["cor"] = value.strip()

    @property
    def tamanho(self):
        return self.data.get("tamanho")

    @tamanho.setter
    def tamanho(self, value):
        self.data["tamanho"] = value.strip() if value else None

    @property
    def material(self):
        return self.data.get("material")

    @material.setter
    def material(self, value):
        self.data["material"] = value.strip() if value else None

    @property
    def detalhes(self):
        return self.data.get("detalhes")

    @detalhes.setter
    def detalhes(self, value):
        self.data["detalhes"] = value.strip() if value else None

    @property
    def foto(self):
        return self.data.get("foto")

    @foto.setter
    def foto(self, value):
        self.data["foto"] = value  # Caminho/nome do arquivo salvo localmente

    @property
    def status(self):
        return self.data.get("status", 1)

    @status.setter
    def status(self, value):
        if value not in self.TIPOS_STATUS:
            raise ValueError("Status inválido.")
        self.data["status"] = int(value)

    @property
    def data_cadastro(self):
        return self.data.get("data_cadastro")  # Automático

    @property
    def data_devolucao(self):
        return self.data.get("data_devolucao")

    @data_devolucao.setter
    def data_devolucao(self, value):
        self.data["data_devolucao"] = value

    @property
    def categoria(self):
        return self.data.get("categoria")

    @categoria.setter
    def categoria(self, value):
        if not value:
            raise ValueError("A categoria é obrigatória.")
        self.data["categoria"] = value

    @property
    def instituicao(self):
        return self.data.get("instituicao")

    @instituicao.setter
    def instituicao(self, value):
        if not value:
            raise ValueError("A instituição é obrigatória.")
        self.data["instituicao"] = value

    @property
    def onde_guardado(self):
        return self.data.get("onde_guardado")

    @onde_guardado.setter
    def onde_guardado(self, value):
        self.data["onde_guardado"] = value

    @property
    def onde_encontrado(self):
        return self.data.get("onde_encontrado")

    @onde_encontrado.setter
    def onde_encontrado(self, value):
        self.data["onde_encontrado"] = value.strip() if value else None

    @property
    def quem_encontrou(self):
        return self.data.get("quem_encontrou")

    @quem_encontrou.setter
    def quem_encontrou(self, value):
        self.data["quem_encontrou"] = value

    @property
    def dono(self):
        return self.data.get("dono")

    @dono.setter
    def dono(self, value):
        self.data["dono"] = value