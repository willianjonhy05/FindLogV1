from flask import Flask
from routes import main_routes
from database.sqlitedb import SQLiteDB
from routes.instituicao_routes import instituicao_rotas
from routes.sala_routes import sala_rotas
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

supabase = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

db = SQLiteDB()
db.conectar() 
db.executar_script_sql('database/scripts/criar_tabelas.sql')
db.desconectar()

main_routes.adicionar_rotas(app)
instituicao_rotas(app)
sala_rotas(app)