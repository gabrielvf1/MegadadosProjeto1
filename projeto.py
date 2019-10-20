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
        cursor.execute('SELECT * FROM Desc_passaros WHERE Nome = %s', (nome))
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
def adiciona_usuario(conn,login,nome,email,cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Usuarios (Login,Nome,Email,Cidade) VALUES (%s,%s,%s,%s)', (login,nome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuario. ERRO : {str(e)}')

#acha um usuario presente no banco de dados atraves do seu login
def acha_usuario(conn, login):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Usuarios WHERE Login = %s', (login))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

# remove um usuario atraves do seu login
def remove_usuario(conn, login):
    with conn.cursor() as cursor:
        try:
            cursor.execute('DELETE FROM Usuarios WHERE Login=%s', (login))
            cursor.execute('UPDATE Posts SET Estado=%s WHERE loginUsuario=%s',('Inativo',login))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel remover {nome} da tabela usuario')

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
        cursor.execute('SELECT Login from Usuarios')
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
def adiciona_post(conn, login,texto,titulo,url="NULL",estado="Ativo",date="NULL",browser="NULL",aparelho="NULL",IP="0.0.0.0"):
    with conn.cursor() as cursor:
        try:
            if(date=="NULL"):
                cursor.execute('INSERT INTO Posts (Texto,Titulo,loginUsuario,URL_IMG,Estado)\
                    VALUES (%s,%s,%s,%s,%s)', (texto,titulo,login,url,estado))
            else:
                cursor.execute('INSERT INTO Posts (Texto,Titulo,loginUsuario,URL_IMG,Estado,Data)\
                    VALUES (%s,%s,%s,%s,%s,%s)', (texto,titulo,login,url,estado,date))
            id_post=acha_post(conn,login,titulo)
            palavras=texto.split()
            for word in palavras:
                if(word[0]=="@"):
                    cursor.execute("""SELECT Login FROM Usuarios WHERE Login LIKE %s""", ('%' + word[1:] + '%',))
                    res = cursor.fetchone()
                    if res:
                        cursor.execute('INSERT INTO User_ref (idPost,loginUsuario) VALUES (%s,%s)', (id_post,word[1:]))
                if(word[0]=="#"):
                    cursor.execute("""SELECT Nome FROM Desc_passaros WHERE Nome LIKE %s""", ('%' + word[1:] + '%',))

                    res = cursor.fetchone()
                    if res:
                        cursor.execute('INSERT INTO Pass_ref (idPost,nomePassaro) VALUES (%s,%s)', (id_post,res[0]))
            adiciona_acao(conn=conn,login=login,nome_acao='adiciona_post',browser=browser,aparelho=aparelho,IP=IP)    




        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel adicionar o post de titulo : {titulo} \
                            na tabela Posts. ERRO : {str(e)}')

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

#adiciona Curtidas
def add_curtida(conn,login,post_id,browser,aparelho,IP):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Curtidas (idPost,loginUsuario,Tipo) VALUES (%s,%s,%s)', (post_id,login,'like'))
            adiciona_acao(conn,login,'curtir',browser,aparelho,IP)
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não foi possivel curtir post {post_id}\
                 usuario {login} {tipo}')

#lista todas as curtidas
def lista_curtidas(conn,post_id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT loginUsuario FROM Curtidas WHERE idPost=%s and Tipo=%s', (post_id,"like"))
        res = cursor.fetchall()

        pessoas = tuple(x[0] for x in res)
        return pessoas

#Lista Usuarios mais Populares de Cada cidade
def lista_user_pop_cidade(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('''
            Select Usuarios.Cidade Regiao,
                    COUNT(Usuarios.Login) Vezes,
                        Usuarios.Login  Pessoa
                    from Usuarios
                INNER JOIN User_ref ON Usuarios.Login = User_ref.loginUsuario
            GROUP BY Usuarios.Cidade, Usuarios.Login
            ORDER BY Vezes DESC
            '''
            )
            res = cursor.fetchall()
            listaRegiao = []
            listaResultado = []
            for i in res:
                if (i[0] in listaRegiao):
                    continue
                listaRegiao.append(i[0])
                listaResultado.append(i)
            populares = tuple(x for x in listaResultado)
            return list(populares)

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não possivel identificar os usuarios mais populares de cada regiao')

#listas posts em ordem cronologica inversa
def lista_post_cron_reverso(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('''Select * FROM Posts
            ORDER BY Data DESC''')
            res = cursor.fetchall()
            return res

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não possivel identificar Posts')

#lista usuarios referenciados
def lista_usr_from_refs(conn,login):
     with conn.cursor() as cursor:
        try:
            cursor.execute('''
                    Select DISTINCT Posts.loginUsuario
                                    from Usuarios
                                INNER JOIN User_ref ON Usuarios.Login = User_ref.loginUsuario
                                INNER JOIN Posts ON User_ref.idPost = Posts.idPost
                                WHERE User_ref.loginUsuario=%s''', (login)
                            )
            res = cursor.fetchall()
            pessoas = tuple(x[0] for x in res)
            return pessoas

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não possivel listar as referencias do usuario {login} ')

#adiciona um tipo de acao
def adiciona_tipo_acao(conn,nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO Tipo_acao (Nome)\
                 VALUES (%s)', (nome))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir a acao de {nome} \
                            na tabela Tipo_acao')

#lista tipos de acoes
def lista_tipo_acoes(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT Nome from Tipo_acao')
        res = cursor.fetchall()
        acoes = tuple(x[0] for x in res)
        return acoes

#adiciona acoes
def adiciona_acao(conn,login,nome_acao,browser,aparelho,IP):
    with conn.cursor() as cursor:
        try:
            if(nome_acao not in list(lista_tipo_acoes(conn))):
                adiciona_tipo_acao(conn,nome_acao)
            cursor.execute('INSERT INTO Acoes (loginUsuario,Nome_acao,Browser,Aparelho,IP)\
                    VALUES (%s,%s,%s,%s,%s)', (login,nome_acao,browser,aparelho,IP))

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir a acao do usuario {login} \
                            na tabela Acoes')

#Tabela cruzada de quantidade de aparelhos por tipo e por browser.
def quantidade_aparelho_browser(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('''
            Select Browser, Aparelho, count(Aparelho) from Acoes
            GROUP BY Acoes.Aparelho, Browser
            '''
            )
            res = cursor.fetchall()
            return list(res)

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Nao foi possivel fazer a tabela de aparelhos por browser')

#Lista com URLs de imagens e respectivos #tags de tipo de pássaro.
def list_url_passaro(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('''SELECT Posts.URL_IMG, nomePassaro FROM Pass_ref LEFT OUTER JOIN Posts USING(idPost)'''
            )
            res = cursor.fetchall()
            return res

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Nao foi possivel achar imagem para passaro')
