import unicodedata
import re

class Categoria:
    def __init__(self, data=None):
        self.data = data or {}
        self.errors = []

        # Status ativo padrão
        if "ativa" not in self.data:
            self.data["ativa"] = True

        # Se for um cadastro novo (sem código/slug definidos), gera de forma única
        nome = self.data.get("nome")
        if nome:
            if not self.data.get("codigo"):
                self.data["codigo"] = self._gerar_codigo_unico(nome)
            if not self.data.get("slug"):
                self.data["slug"] = self._gerar_slug_unico(nome)

    def __str__(self):
        return self.data.get("nome", "Nome não definido")

    def validate(self, is_new=True):
        self.errors = []
        
        # Validação do nome
        nome = self.data.get("nome")
        if not nome or not nome.strip():
            self.errors.append("O nome da categoria não pode ser vazio.")
        
        # Validação da descrição
        descricao = self.data.get("descricao")
        if not descricao or not descricao.strip():
            self.errors.append("A descrição não pode ser vazia.")

        # Validação extra de unicidade caso tenha sido passado manualmente
        if is_new:
            codigo = self.data.get("codigo")
            slug = self.data.get("slug")
            
            if codigo and Categoria.get_by_codigo(codigo):
                self.errors.append("Já existe uma categoria cadastrada com este código.")
            if slug and Categoria.get_by_slug(slug):
                self.errors.append("Já existe uma categoria cadastrada com este slug.")

        return len(self.errors) == 0

    def save(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.add_categoria(self)

    @staticmethod
    def _gerar_slug(nome):
        """Converte o nome em um slug amigável para URLs"""
        if not nome:
            return ""
        nfkd_form = unicodedata.normalize('NFKD', nome)
        texto_sem_acento = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        
        slug = texto_sem_acento.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s-]+', '-', slug).strip('-')
        return slug

    @classmethod
    def _gerar_slug_unico(cls, nome):
        """Garante que o slug gerado seja único no banco de dados"""
        base_slug = cls._gerar_slug(nome)
        slug = base_slug
        contador = 1
        
        # Enquanto o slug já existir no banco, adiciona um sufixo numérico (-1, -2...)
        while cls.get_by_slug(slug):
            slug = f"{base_slug}-{contador}"
            contador += 1
            
        return slug

    @staticmethod
    def _gerar_codigo_inicial(nome):
        """Gera as duas primeiras letras do nome em maiúsculo + dois números padrão (ex: TE01)"""
        if not nome or len(nome.strip()) < 2:
            return "XX01"
        
        limpo = nome.strip().upper()
        letras = re.sub(r'[^A-Z]', '', limpo)[:2]
        if len(letras) < 2:
            letras = (letras + 'X')[:2]
            
        return f"{letras}"

    @classmethod
    def _gerar_codigo_unico(cls, nome):
        """Garante que o código gerado seja único no banco incrementando o número"""
        base_letras = cls._gerar_codigo_inicial(nome)
        contador = 1
        
        while True:
            codigo = f"{base_letras}{contador:02d}" # Ex: TE01, TE02...
            if not cls.get_by_codigo(codigo):
                return codigo
            contador += 1
            if contador > 99: # Caso ultrapasse 99, expande para 3 dígitos
                codigo = f"{base_letras}{contador}"
                if not cls.get_by_codigo(codigo):
                    return codigo

    @staticmethod
    def get_all():
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categorias()

    @staticmethod
    def get_all_activas():
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categorias_ativas()

    @staticmethod
    def get_by_codigo(codigo):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categoria_by_codigo(codigo)

    @staticmethod
    def get_by_slug(slug):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categoria_by_slug(slug)

    def delete(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        dao.deletar_categoria(self.codigo)

    def update(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        dao.atualizar_categoria(self)

    @staticmethod
    def contar_total():
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.contar_total()

    @staticmethod
    def contar_por_status(ativa=True):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.contar_por_status(ativa)

    @staticmethod
    def obter_estatisticas():
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return {
            "total": dao.contar_total(),
            "ativas": dao.contar_por_status(True),
            "inativas": dao.contar_por_status(False)
        }

    @property
    def nome(self):
        return self.data.get("nome")

    @nome.setter
    def nome(self, value):
        if not value or not value.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")
        self.data["nome"] = value.strip()
        # Nota: Slug e Código continuam imutáveis após a criação.

    @property
    def codigo(self):
        return self.data.get("codigo")

    @property
    def slug(self):
        return self.data.get("slug")       

    @property
    def descricao(self):
        return self.data.get("descricao")

    @descricao.setter
    def descricao(self, value):
        if not value or not value.strip():
            raise ValueError("A descrição não pode ser vazia.")
        self.data["descricao"] = value.strip()

    @property
    def ativa(self):
        return self.data.get("ativa", True)

    @ativa.setter
    def ativa(self, value):
        if not isinstance(value, bool):
            raise ValueError("O status deve ser booleano.")
        self.data["ativa"] = value