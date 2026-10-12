from flask import Flask
from routes import main_routes
from database.sqlitedb import SQLiteDB
from routes.instituicao_routes import instituicao_rotas
from routes.sala_routes import sala_rotas
from routes.categoria_routes import categoria_routes
from routes.usuario_routes import usuario_routes
from routes.item_routes import item_rotas
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_sitemap import Sitemap

load_dotenv()

app = Flask(__name__)
ext = Sitemap(app=app)

app.secret_key = os.environ.get('SECRET_KEY')

supabase = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

# db = SQLiteDB()
# db.conectar() 
# db.executar_script_sql('database/scripts/criar_tabelas.sql')
# db.desconectar()

main_routes.adicionar_rotas(app)
instituicao_rotas(app)
categoria_routes(app)
item_rotas(app)
usuario_routes(app)
sala_rotas(app)

if __name__ == "__main__":
    app.run()