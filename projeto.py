import pymysql

# funcao adiciona um unico passaro
def adiciona_passaro(conn, nome,cor="NULL",
                        comida="NULL",onde_vive="NULL",
                        tamanho="NULL"):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Desc_passaros (Nome,Cor,Comida,Onde_vive,Tamanho)\
                 VALUES (%s,%s,%s,%s,%s)', (nome,cor,comida,onde_vive,tamanho))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o passarinho {nome} \
                            na tabela Desc_passaros')

#acha o primeiro passaro com este nome 
def acha_passaro(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Nome,Cor,Comida,Onde_vive,Tamanho FROM Desc_passaros WHERE Nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

#remove o passaro
def remove_passaro(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Desc_passaros WHERE Nome=%s', (nome))

#seleciona os nomes dos passaros existentes na base 
def lista_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Nome from Desc_passaros')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros
#Adiona um usuario ao banco utilizando como entrada login e nome sendo obrigatorios
def adiciona_usuario(conn,login,nome,email="NULL",cidade="NULL"):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Usuarios (Login,Nome,Email,Cidade) VALUES (%s,%s,%s,%s)', (login,nome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuario')
            
            
#acha um usuario presente no banco de dados atraves do seu login
def acha_usuario(conn, login):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Nome FROM Usuarios WHERE Login = %s', (login))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None
# remove um usuario atraves do seu login
def remove_usuario(conn, login):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Usuarios WHERE Login=%s', (login))
        cursor.execute('UPDATE Posts SET Estado=%s WHERE loginUsuario=%s',('Inativo',login))

#muda o email de um usuario no banco de dados, recebendo login e o novo email que deve ser inserido
def muda_email_usuario(conn, login, novo_email):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE Usuarios SET Email=%s where Login=%s', (novo_email, login))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar o Email do id {login} para {novo_email} na tabela Usuarios')
# Lista os usuarios presentes na base
def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Nome from Usuarios')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios
# Acha um post de um usuario , o mesmo precisa do login do usario e do titulo para diferenciar de outros posts do mesmo usuario
def acha_post(conn, login, titulo):
   with conn.cursor() as cursor:
        cursor.execute('SELECT idPost FROM Posts WHERE Titulo = %s AND loginUsuario = %s ', (titulo, login))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None
# Insere um post novo ao banco. Reconhecendo quem foi marcado e passaros referenciados. Aqui a logica de adicionar em todas tabelas
def adiciona_post(conn, login,texto,titulo,url,estado="Ativo"):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Posts (Texto,Titulo,loginUsuario,URL_IMG,Estado)\
                 VALUES (%s,%s,%s,%s,%s)', (texto,titulo,login,url,estado))
            id_post=acha_post(conn,login,titulo)
            palavras=texto.split()
            for word in palavras:
                if(word[0]=="@"):
                    cursor.execute('INSERT INTO User_ref (idPost,loginUsuario) VALUES (%s,%s)', (id_post,word[1:]))
                if(word[0]=="#"):
                    cursor.execute("""SELECT Nome FROM Desc_passaros WHERE Nome LIKE %s""", ('%' + word[1:] + '%',))
                    
                    res = cursor.fetchone()
                    if res:
                        cursor.execute('INSERT INTO Pass_ref (idPost,nomePassaro) VALUES (%s,%s)', (id_post,res[0]))
    



        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel adicionar o post de titulo : {titulo} \
                            na tabela Posts')

#funcao que faz o delete logico do post, ou seja para remover um post voce deve realizar um update na coluna Estado para inativo.
def remove_post(conn, login, postid): 
    with conn.cursor() as cursor:
        cursor.execute('UPDATE Posts SET Estado=%s WHERE idPost=%s',('Inativo',postid))
    
#lista quais usuarios foram citados em um post especifico, recebendo o id do post
def lista_post_ref_user(conn,idPost):
    with conn.cursor() as cursor:
        cursor.execute('SELECT User_ref.loginUsuario from User_ref INNER JOIN Posts USING(idPost) WHERE User_ref.idPost=%s and Posts.Estado=%s' , (idPost, "Ativo"))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None
#lista no post os passaros referenciados
def lista_post_ref_pass(conn,idPost):
    with conn.cursor() as cursor:
        cursor.execute('SELECT nomePassaro from Pass_ref INNER JOIN Posts USING(idPost) WHERE Pass_ref.idPost=%s and Posts.Estado=%s', (idPost, "Ativo"))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None
# Ve todas referencias ativas do usuario 
def lista_usr_ref_posts(conn, login):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Posts.idPost from User_ref INNER JOIN Posts USING(idPost) WHERE Posts.Estado=%s and User_ref=%s' , ("Ativo",login))
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

#remove uma preferencia de um usuario em um passaro da tabela pref_pass, recebendo o login e o passaro
def remove_pref_pass(conn, login, passaro):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM Pref_pass WHERE loginUsuario=%s and nomePassaro=%s', (login,passaro))

#adicona uma preferencia do usuario em um passaro na tabela pref_pass recebendo o usuario e o passaro a ser favoritado
def adiciona_pref_pass(conn,login,passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Pref_pass (loginUsuario,nomePassaro) VALUES (%s,%s)', (login,passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir este passaro {passaro}\
                 como preferencia do {login} na tabela Pref_pass')

#lista quais passaros determinado usuario tem como favorito, recebendo o login do usuario.
def lista_pref_usr_pass(conn,login):
    with conn.cursor() as cursor:
        cursor.execute('SELECT nomePassaro FROM Pref_pass WHERE loginUsuario=%s', (login))
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

# def adiciona_perigo_a_comida(conn, id_perigo, id_comida):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO comida_perigo VALUES (%s, %s)', (id_comida, id_perigo))

# def remove_perigo_de_comida(conn, id_perigo, id_comida):
#     with conn.cursor() as cursor:
#         cursor.execute('DELETE FROM comida_perigo WHERE id_perigo=%s AND id_comida=%s',(id_perigo, id_comida))

# def lista_comidas_de_perigo(conn, id_perigo):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_comida FROM comida_perigo WHERE id_perigo=%s', (id_perigo))
#         res = cursor.fetchall()
#         comidas = tuple(x[0] for x in res)
#         return comidas

# def lista_passaros_de_comida(conn, id_comida):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_perigo FROM comida_perigo WHERE id_comida=%s', (id_comida))
#         res = cursor.fetchall()
#         perigos = tuple(x[0] for x in res)
#         return perigos
