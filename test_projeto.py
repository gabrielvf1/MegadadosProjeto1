import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

from projeto import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='mydb'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_adiciona_passaro(self):
        conn = self.__class__.connection
    
        passaro = 'beija flor'

        # Adiciona um passaro não existente.
        adiciona_passaro(conn, passaro)

        # Checa se o passaro existe.
        id = acha_passaro(conn, passaro)
        self.assertIsNotNone(id)

        # Tenta achar um passaro inexistente.
        id = acha_passaro(conn, 'carvalho branco')
        self.assertIsNone(id)

    def test_remove_passaro(self):
        conn = self.__class__.connection
        adiciona_passaro(conn, 'canario azul')
        info = acha_passaro(conn, 'canario azul')

        res = lista_passaros(conn)
        self.assertCountEqual(res, (info,))

        remove_passaro(conn, info)

        res = lista_passaros(conn)
        self.assertFalse(res)

    def test_lista_passaros(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem passaros no sistema.
        res = lista_passaros(conn)
        self.assertFalse(res)

        # Adiciona alguns passaros.
        passaros = []
        for p in ('canario', 'cacatua', 'canario da terra'):
            adiciona_passaro(conn, p)
            passaros.append(p)

        # Verifica se os passaros foram adicionados corretamente.
        res = lista_passaros(conn)
        self.assertCountEqual(res, passaros)

        # Remove os passaros.
        for p in passaros:
            remove_passaro(conn, p)

        # Verifica que todos os passaros foram removidos.
        res = lista_passaros(conn)
        self.assertFalse(res)

    def test_adiciona_usuario(self):
        conn = self.__class__.connection

        usuario = {"loginUsuario":'Antoniojaj',"Nome":'Antonio Andraues'}

        # Adiciona se usuario não existente.
        adiciona_usuario(conn, login='Antoniojaj', nome='Antonio Andraues')

        # Checa se o usuario existe.
        nome = acha_usuario(conn, 'Antoniojaj')
        self.assertIsNotNone(nome)

        # Tenta achar um usuario inexistente.
        nome = acha_usuario(conn, 'Gabriel')
        self.assertIsNone(nome)

    def test_remove_usuario(self):

        conn = self.__class__.connection
        adiciona_usuario(conn, 'gabrielvf', 'Gabriel Francato')
        nome = acha_usuario(conn, 'gabrielvf')

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (nome,))

        remove_usuario(conn, 'gabrielvf')

        res = lista_usuarios(conn)
        self.assertFalse(res)

    def test_muda_email_usuario(self):
        conn = self.__class__.connection

        adiciona_usuario(conn, login='antonio',nome='Antonio Andraues',email="teste@a.com")

        muda_email_usuario(conn, login='antonio', novo_email='antonio@teste.com')

    def test_lista_usuarios(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem nenhum usuario no sistema.
        res = lista_usuarios(conn)
        self.assertFalse(res)

        # Adiciona alguns usuarios.
        nomes = []
        for p in ('antonio', 'gabriel', 'teste'):
            adiciona_usuario(conn, p,"Nome teste")
            nomes.append(acha_usuario(conn, p))

        # Verifica se os usuarios foram adicionadas corretamente.
        res = lista_usuarios(conn)
        self.assertCountEqual(res, nomes)

        # Remove os usuarios.
        for c in ('antonio', 'gabriel', 'teste'):
            remove_usuario(conn, c)

        # Verifica que todos as usuarios foram removidos.
        res = lista_usuarios(conn)
        self.assertFalse(res)

    def test_post_ref(self):
        conn = self.__class__.connection
    
        titulo="teste 123"
        creador='antoniojaj'
        adiciona_usuario(conn, login=creador,nome='Antonio Andraues',email="teste@a.com")
        adiciona_usuario(conn, login='gabriel',nome='Gabriel Francato',email="teste@a.com")
        # Adiciona um post
        adiciona_post(conn=conn,login=creador,texto="DEMAIS ESSE PASSARO @gabriel",titulo=titulo,url="NULL",estado="Ativo")
        id_post=acha_post(conn,login=creador,titulo=titulo)

        res=lista_post_ref_user(conn,id_post)
        self.assertEqual(first=res,second='gabriel')
        
    def test_post_ref_passaro(self):
        conn = self.__class__.connection
        
        titulo="teste passaro ref"
        creador='antoniojaj'
        adiciona_usuario(conn, login=creador,nome='Antonio Andraues',email="teste@a.com")
        passaro = 'canario da terra'

        # Adiciona um passaro não existente.
        adiciona_passaro(conn, passaro)
        # Adiciona um post
        adiciona_post(conn=conn,login=creador,texto="DEMAIS ESSE PASSARO #canario",titulo=titulo,url="NULL",estado="Ativo")
        id_post=acha_post(conn,login=creador,titulo=titulo)

        res=lista_post_ref_pass(conn,id_post)

        self.assertEqual(first=res,second=passaro)


    def test_adiciona_pref_pass(self):
        conn = self.__class__.connection
        creador='antoniojaj'
        adiciona_usuario(conn, login=creador,nome='Antonio Andraues',email="teste@a.com")

        # Nehuma pref
        res = lista_pref_usr_pass(conn,creador)
        self.assertCountEqual(res, [])
        
         # Adiciona alguns passaros.
        passaros = []
        for p in ('canario', 'cacatua', 'canario da terra'):
            adiciona_passaro(conn, p)
            adiciona_pref_pass(conn,creador,p)
            passaros.append(p)


        # Checando as preferencias
        res = lista_pref_usr_pass(conn,creador)
        self.assertCountEqual(res, passaros)
        self.assertEqual(res[0],passaros[0])
        self.assertEqual(res[1],passaros[1])
        self.assertEqual(res[2],passaros[2])
        

    def test_remove_pref_pass(self):
        conn = self.__class__.connection
        creador='antoniojaj'
        passaro='canario da terra'
        adiciona_usuario(conn, login=creador,nome='Antonio Andraues',email="teste@a.com")
        adiciona_passaro(conn,passaro)
        adiciona_pref_pass(conn,creador,passaro)

        # Checa que ele foi removido corretamente 
        remove_pref_pass(conn, login=creador,passaro=passaro)
        res=lista_pref_usr_pass(conn,creador)
        self.assertCountEqual(res, [])


def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)