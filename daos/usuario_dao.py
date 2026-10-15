class UsuarioDAO:

    def get_usuarios(self):
        from main import supabase
        from models.usuario import Usuario
        
        response = supabase.table('usuarios').select("*").execute()
        usuarios = []
        
        data_rows = response.data if hasattr(response, 'data') else response
        
        for row in data_rows:
            # Mapeia as colunas do banco para as chaves internas que o modelo Usuario espera
            row_data = row.copy()
            row_data["instituicao"] = row.get("instituicao_cnpj")
            row_data["sala"] = row.get("sala_codigo")
            
            usuario = Usuario(data=row_data)
            usuarios.append(usuario)
            
        return usuarios

    def add_usuario(self, usuario):
        from main import supabase
        
        dados = {
            "username": usuario.username,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "senha": usuario.senha,
            "cpf": usuario.cpf,
            "data_nascimento": str(usuario.data_nascimento),
            "data_cadastro": str(usuario.data_cadastro),
            "tipo_usuario": int(usuario.tipo_usuario),
            "ativo": bool(usuario.ativo),
            "foto_perfil": usuario.foto_perfil,
            "instituicao_cnpj": usuario.instituicao,
            "sala_codigo": usuario.sala # Pode ser None se for Administrador ou Usuário Comum
        }
        
        try:
            resposta = supabase.table("usuarios").insert(dados).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao adicionar usuário: {erro}")
            return None

    def get_usuario_by_username(self, username):
        from main import supabase
        from models.usuario import Usuario
        
        try:
            resposta = supabase.table("usuarios").select("*").eq("username", username).execute()
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta
            
            if data_rows and len(data_rows) > 0:
                row = data_rows[0]
                row_data = row.copy()
                row_data["instituicao"] = row.get("instituicao_cnpj")
                row_data["sala"] = row.get("sala_codigo")
                return Usuario(data=row_data)
        except Exception as erro:
            print(f"Erro ao buscar usuário por username: {erro}")
            
        return None

    def get_usuario_by_email(self, email):
        from main import supabase
        from models.usuario import Usuario

        try:
            resposta = supabase.table("usuarios").select("*").eq("email", email).execute()
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta

            if data_rows and len(data_rows) > 0:
                row = data_rows[0]
                row_data = row.copy()
                row_data["instituicao"] = row.get("instituicao_cnpj")
                row_data["sala"] = row.get("sala_codigo")
                return Usuario(data=row_data)
        except Exception as erro:
            print(f"Erro ao buscar usuário por email: {erro}") # <--- Corrigido a mensagem

        return None


    def get_usuario_by_cpf(self, cpf):
        from main import supabase
        from models.usuario import Usuario
        
        try:
            resposta = supabase.table("usuarios").select("*").eq("cpf", cpf).execute()
            data_rows = resposta.data if hasattr(resposta, 'data') else resposta
            
            if data_rows and len(data_rows) > 0:
                row = data_rows[0]
                row_data = row.copy()
                row_data["instituicao"] = row.get("instituicao_cnpj")
                row_data["sala"] = row.get("sala_codigo")
                return Usuario(data=row_data)
        except Exception as erro:
            print(f"Erro ao buscar usuário por CPF: {erro}")
            
        return None

    def atualizar_usuario(self, usuario):
        from main import supabase
        
        dados = {
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "senha": usuario.senha,
            "cpf": usuario.cpf,
            "data_nascimento": str(usuario.data_nascimento),
            "tipo_usuario": int(usuario.tipo_usuario),
            "ativo": bool(usuario.ativo),
            "foto_perfil": usuario.foto_perfil,
            "instituicao_cnpj": usuario.instituicao,
            "sala_codigo": usuario.sala
        }
        
        try:
            # O username é a chave primária, portanto usamos ele na cláusula eq
            resposta = supabase.table("usuarios").update(dados).eq("username", usuario.username).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao atualizar usuário: {erro}")
            return None

    def atualizar_dados_perfil(self, username, dados):
        from main import supabase
        
        # Filtra apenas os campos permitidos por segurança
        campos_permitidos = {
            "nome": dados.get("nome"),
            "email": dados.get("email"),
            "telefone": dados.get("telefone"),
            "data_nascimento": dados.get("data_nascimento")
        }

        if dados.get("foto_perfil"):
            campos_permitidos["foto_perfil"] = dados.get("foto_perfil")
        
        # Remove valores nulos ou vazios se necessário, ou envia diretamente
        response = supabase.table('usuarios').update(campos_permitidos).eq('username', username).execute()
        
        if response.data or hasattr(response, 'data'):
            return True, "Dados atualizados com sucesso."
            
        return False, "Erro ao atualizar os dados no banco de dados."
        

    def deletar_usuario(self, username):
        from main import supabase
        
        try:
            resposta = supabase.table("usuarios").delete().eq("username", username).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao deletar usuário: {erro}")
            return None


    def contar_total(self):
        from main import supabase
        try:
            resposta = supabase.table("usuarios").select("*", count="exact", head=True).execute()
            return resposta.count if resposta.count is not None else 0
        except Exception as e:
            print(f"Erro ao contar total de usuários: {e}")
            return 0


    def qtd_usuarios_na_instituicao(self, cnpj):
        from main import supabase

        try:
            resposta = supabase.table("usuarios").select("*", count="exact", head=True).eq("instituicao_cnpj", cnpj).execute()
            return resposta.count if resposta.count is not None else 0

        except Exception as e:
            print(f"Erro ao contar total de usuários: {e}")
            return 0

    def get_usuarios_by_instituicao(self, cnpj):
        from main import supabase
        from models.usuario import Usuario
        
        response = supabase.table('usuarios').select("*").eq("instituicao_cnpj", cnpj).execute()
        usuarios = []
        
        data_rows = response.data if hasattr(response, 'data') else response
        
        for row in data_rows:
            # Mapeia as colunas do banco para as chaves internas que o modelo Usuario espera
            row_data = row.copy()
            row_data["instituicao"] = row.get("instituicao_cnpj")
            row_data["sala"] = row.get("sala_codigo")
            
            usuario = Usuario(data=row_data)
            usuarios.append(usuario)
            
        return usuarios            
    


    def atualizar_senha(self, username, senha_atual, nova_senha):
        from main import supabase
        from werkzeug.security import check_password_hash, generate_password_hash
        
        # Busca o usuário no banco para verificar a senha atual
        response = supabase.table('usuarios').select("*").eq('username', username).execute()
        data_rows = response.data if hasattr(response, 'data') else []
        
        if not data_rows:
            return False, "Usuário não encontrado."
            
        user_data = data_rows[0]
        
        # Verifica se a senha atual confere (compatível com hash)
        if not check_password_hash(user_data.get('senha', ''), senha_atual):
            return False, "A senha atual está incorreta."
            
        # Gera o hash da nova senha
        nova_senha_hash = generate_password_hash(nova_senha)
        
        # Atualiza no Supabase
        update_response = supabase.table('usuarios').update({'senha': nova_senha_hash}).eq('username', username).execute()
        
        if update_response.data or hasattr(update_response, 'data'):
            return True, "Senha alterada com sucesso."
            
        return False, "Erro ao atualizar senha no banco de dados."    