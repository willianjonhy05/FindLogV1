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

    def deletar_usuario(self, username):
        from main import supabase
        
        try:
            resposta = supabase.table("usuarios").delete().eq("username", username).execute()
            data_resposta = resposta.data if hasattr(resposta, 'data') else resposta
            return data_resposta[0] if data_resposta else None
        except Exception as erro:
            print(f"Erro ao deletar usuário: {erro}")
            return None