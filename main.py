from flask import Flask
from routes import main_routes
from database.sqlitedb import SQLiteDB
from routes.instituicao_routes import instituicao_rotas

app = Flask(__name__)


db = SQLiteDB()
db.conectar() 
db.executar_script_sql('database/scripts/criar_tabelas.sql')
db.desconectar()

main_routes.adicionar_rotas(app)
instituicao_rotas(app)