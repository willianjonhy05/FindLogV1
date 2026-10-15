from datetime import date


def verificar_maioridade(data_nascimento):
  # Se receber uma string no formato 'YYYY-MM-DD', converte para date
  if isinstance(data_nascimento, str):
    data_nascimento = date.fromisoformat(data_nascimento)

  hoje = date.today()

  # Calcula a diferença em anos
  idade = hoje.year - data_nascimento.year

  # Ajusta caso o aniversário ainda não tenha ocorrido este ano
  aniversario_ainda_nao_passou = (hoje.month, hoje.day) < (
      data_nascimento.month,
      data_nascimento.day,
  )
  if aniversario_ainda_nao_passou:
    idade -= 1

  # Retorna False se menor de 18 anos, True caso contrário
  return idade >= 18

