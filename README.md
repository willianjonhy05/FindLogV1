# FindLog V1

Sistema de gerenciamento de achados e perdidos desenvolvido para instituições e empresas.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o projeto localmente em sua máquina (ambiente Windows):

### Passo 1
Escolha e acesse uma pasta de sua preferência no seu computador.

### Passo 2
Abra o terminal na pasta escolhida e execute o comando para clonar o repositório:

```
git clone https://github.com/willianjonhy05/FindLogV1.git
```

### Passo 3
Entre na pasta do projeto recém-criada:

```
cd FindLogV1
```

### Passo 4
Crie e ative o ambiente virtual Python executando os comandos:

```
python -m venv venv
./venv/Scripts/activate

```

### Passo 5
Com o ambiente virtual ativado, instale as dependências do projeto:

```
pip install -r requirements.txt
```

### Passo 6

Entre no site https://randomkeygen.com/flask-secret-key e gere uma chave secreta. Copie o código, vá no seu arquivo .env e crie a seguinte variável: 


```
SECRET_KEY=cole_aqui_o_codigo gerado

```

### Passo 7

Entre em contato com o William para preecher corretamente outras variáveis do arquivo .env


### Passo 8

Para rodar o sistema localmente em modo de desenvolvimento, execute o comando:

```
flask --app main run --debug
```

### Passo 9

Acesse o endereço: http://localhost:5000/usuario/novo preencha corretamente todos os campos para criar um usuário.

Obs: Em Instituição, seleciona a Primeira Classe, em Tipo de Usuário escolha administrador; a foto não é obrigatória.


Se obtiver algum erro, por favor, faça print da página e entre em contato imediatamente com o William


Pronto! O sistema estará rodando e disponível para acesso no seu navegador através do endereço gerado pelo Flask.

Projeto desenvolvido pela Equipe Primeira Classe de Desenvolvimento.
