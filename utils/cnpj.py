import re

def validar_cnpj(cnpj: str):
    if not isinstance(cnpj, str):
        return "O CNPJ deve ser um texto válido."
    
    # Remove caracteres especiais e converte para maiúsculas
    clean = re.sub(r'[^a-zA-Z0-9]', '', cnpj).upper()
    
    # Verifica se tem exatamente 14 caracteres
    if len(clean) != 14:
        return "O CNPJ deve ter exatamente 14 caracteres."
        
    # Os dois últimos dígitos verificadores devem ser numéricos
    if not clean[12:].isdigit():
        return "Os dois últimos dígitos verificadores devem ser numéricos."

    # Converte caractere para valor numérico usando ASCII - 48
    def char_valor(c):
        return ord(c) - 48

    # Pesos para o primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = sum(char_valor(clean[i]) * pesos1[i] for i in range(12))
    resto1 = soma1 % 11
    dv1 = 0 if resto1 < 2 else 11 - resto1
    
    if char_valor(clean[12]) != dv1:
        return "O primeiro dígito verificador não é válido."

    # Pesos para o segundo dígito verificador (inclui o primeiro DV)
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma2 = sum(char_valor(clean[i]) * pesos2[i] for i in range(13))
    resto2 = soma2 % 11
    dv2 = 0 if resto2 < 2 else 11 - resto2
    
    if char_valor(clean[13]) != dv2:
        return "O segundo dígito verificador não é válido."

    return True
