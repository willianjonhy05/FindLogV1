import unicodedata
import re

class Categoria:
    def __init__(self, nome, descricao, codigo=None, slug=None):
        self.nome = nome
        self.ativa = True
        self.descricao = descricao
        
        self._codigo = codigo if codigo else self._gerar_codigo_inicial(nome)
        self._slug = slug if slug else self._gerar_slug(nome)

    def __str__(self):
        return self.nome

    def save(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.add_categoria(self)


    @staticmethod
    def _gerar_slug(nome):
        """Converte o nome em um slug amigável para URLs (ex: 'Tecnologia da Informação' -> 'tecnologia-da-informacao')"""
        if not nome:
            return ""
        # Normaliza para remover acentos
        nfkd_form = unicodedata.normalize('NFKD', nome)
        texto_sem_acento = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        
        # Converte para minúsculas, remove caracteres especiais e substitui espaços por hífens
        slug = texto_sem_acento.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s-]+', '-', slug).strip('-')
        return slug

    @staticmethod
    def _gerar_codigo_inicial(nome):
        """Gera as duas primeiras letras do nome em maiúsculo + dois números padrão (ex: TE01)"""
        if not nome or len(nome.strip()) < 2:
            return "XX01"
        
        limpo = nome.strip().upper()
        # Pega as 2 primeiras letras (ignorando espaços ou caracteres especiais iniciais se necessário)
        letras = re.sub(r'[^A-Z]', '', limpo)[:2]
        if len(letras) < 2:
            letras = (letras + 'X')[:2]
            
        return f"{letras}01"        

    @staticmethod
    def get_all():
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categorias()

    @staticmethod
    def get_by_codigo(codigo):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categoria_by_codigo(codigo)

    def delete(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        dao.deletar_categoria(self.codigo)

    def update(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        dao.atualizar_categoria(self)

    # ==========================
    # NOME
    # ==========================

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        if not value or not value.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")

        self._nome = value.strip()

    # ==========================
    # CÓDIGO
    # ==========================

    @property
    def codigo(self):
        return self._codigo

    # ==========================
    # SLUG (Imutável - Apenas Getter)
    # ==========================
    @property
    def slug(self):
        return self._slug        


    # ==========================
    # DESCRIÇÃO
    # ==========================

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        if not value or not value.strip():
            raise ValueError("A descrição não pode ser vazia.")

        self._descricao = value.strip()


    # ==========================
    # ATIVA
    # ==========================
    @property
    def ativa(self):
        return self._ativa

    @ativa.setter
    def ativa(self, value):
        if not isinstance(value, bool):
            raise ValueError("O status deve ser booleano.")
        self._ativa = value        