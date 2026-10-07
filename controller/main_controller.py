from flask import render_template, request


def index():
    return render_template('public/index.html')


# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     elif request.method == 'POST':
#         email = request.form.get("email")
#         senha = request.form.get("senha")
#         return "Login realizado com sucesso!"
#     else:
#         return "Método não permitido", 405
