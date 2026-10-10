import os
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/upload/perfis'
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp'}

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

def salvar_foto_perfil(file_storage, username):
    """
    Recebe o objeto FileStorage do request.files e o username do usuário.
    Salva na pasta local e retorna apenas o nome/caminho relativo do arquivo.
    """
    if not file_storage or file_storage.filename == '':
        return None

    if arquivo_permitido(file_storage.filename):
        # Garante que o diretório existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Pega a extensão original do arquivo
        extensao = file_storage.filename.rsplit('.', 1)[1].lower()
        
        # Cria um nome único usando o username do usuário (ex: 'maria.silva.jpg')
        nome_arquivo = f"{username}.{extensao}"
        caminho_completo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        
        # Salva o arquivo fisicamente na pasta
        file_storage.save(caminho_completo)
        
        # Retorna o caminho relativo que será salvo no banco de dados (ex: 'upload/perfis/maria.silva.jpg')
        return f"upload/perfis/{nome_arquivo}"
        
    return None



def salvar_foto_item(file_storage, codigo_item):
    """Salva a foto do item na pasta local static/upload/itens e retorna o caminho relativo."""
    if not file_storage or file_storage.filename == '':
        return None

    upload_folder = 'static/upload/itens'
    extensoes_permitidas = {'png', 'jpg', 'jpeg', 'webp'}
    
    filename = file_storage.filename
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in extensoes_permitidas:
        os.makedirs(upload_folder, exist_ok=True)
        extensao = filename.rsplit('.', 1)[1].lower()
        nome_arquivo = f"{codigo_item}.{extensao}"
        caminho_completo = os.path.join(upload_folder, nome_arquivo)
        
        file_storage.save(caminho_completo)
        return f"upload/itens/{nome_arquivo}"
        
    return None