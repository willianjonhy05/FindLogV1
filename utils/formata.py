def formatar(texto):
    if not isinstance(texto, str):
        texto = str(texto) if texto is not None else ""
    return "".join(c for c in texto if c.isalnum())