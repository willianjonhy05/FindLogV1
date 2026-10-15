import random
import string

def gerar_codigo():
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choices(caracteres, k=5))
    return codigo