import re


def validar_email(email):
    if not isinstance(email, str):
        return "O e-mail informado não é válido."
        
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(padrao, email):
        return True
    return "O e-mail informado não é válido."

