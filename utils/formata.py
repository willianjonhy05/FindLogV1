import re

def formatar(texto):
    if not isinstance(texto, str):
        texto = str(texto) if texto is not None else ""
    return "".join(c for c in texto if c.isalnum())


def limpar_string(texto):
    if not texto:
        return ""
    padrao = r'[.()/\-\s]'
    return re.sub(padrao, '', texto)