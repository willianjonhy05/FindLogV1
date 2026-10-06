import os
import mysql.connector
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env localizado na raiz do projeto
load_dotenv()

def conectar_banco():
    """Estabelece e retorna a conexão com o MySQL utilizando as credenciais do .env"""
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None