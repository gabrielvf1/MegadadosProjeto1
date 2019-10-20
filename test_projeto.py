import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql
import time
import datetime

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

        usuario = {"loginUsuario": 'Antoniojaj', "Nome": 'Antonio Andraues'}

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

        adiciona_usuario(conn, login='antonio',
                         nome='Antonio Andraues', email="teste@a.com")

        muda_email_usuario(conn, login='antonio',
                           novo_email='antonio@teste.com')

    def test_lista_usuarios(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem nenhum usuario no sistema.
        res = lista_usuarios(conn)
        self.assertFalse(res)

        # Adiciona alguns usuarios.
        nomes = []
        for p in ('antonio', 'gabriel', 'teste'):
            adiciona_usuario(conn, p, "Nome teste")
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
        titulo = "teste 123"
        creador = 'antoniojaj'
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', email="teste@a.com")
        adiciona_usuario(conn, login='gabriel',
                         nome='Gabriel Francato', email="teste@a.com")
        # Adiciona um post
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO @gabriel", titulo=titulo,
                      url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        id_post = acha_post(conn, login=creador, titulo=titulo)

        res = lista_post_ref_user(conn, id_post)
        self.assertEqual(first=res, second='gabriel')

    def test_post_ref_passaro(self):
        conn = self.__class__.connection

        titulo = "teste passaro ref"
        creador = 'antoniojaj'
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', email="teste@a.com")
        passaro = 'canario da terra'

        # Adiciona um passaro não existente.
        adiciona_passaro(conn, passaro)
        # Adiciona um post
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO #canario", titulo=titulo,
                      url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        id_post = acha_post(conn, login=creador, titulo=titulo)

        res = lista_post_ref_pass(conn, id_post)

        self.assertEqual(first=res, second=passaro)

    def test_adiciona_pref_pass(self):
        conn = self.__class__.connection
        creador = 'antoniojaj'
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', email="teste@a.com")

        # Nehuma pref
        res = lista_pref_usr_pass(conn, creador)
        self.assertCountEqual(res, [])

        # Adiciona alguns passaros.
        passaros = []
        for p in ('canario', 'cacatua', 'canario da terra'):
            adiciona_passaro(conn, p)
            adiciona_pref_pass(conn, creador, p)
            passaros.append(p)

        # Checando as preferencias
        res = lista_pref_usr_pass(conn, creador)
        self.assertCountEqual(res, passaros)
        self.assertEqual(res[0], passaros[0])
        self.assertEqual(res[1], passaros[1])
        self.assertEqual(res[2], passaros[2])

    def test_remove_pref_pass(self):
        conn = self.__class__.connection
        creador = 'antoniojaj'
        passaro = 'canario da terra'
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', email="teste@a.com")
        adiciona_passaro(conn, passaro)
        adiciona_pref_pass(conn, creador, passaro)

        # Checa que ele foi removido corretamente
        remove_pref_pass(conn, login=creador, passaro=passaro)
        res = lista_pref_usr_pass(conn, creador)
        self.assertCountEqual(res, [])

    def test_add_curtidas(self):
        conn = self.__class__.connection
        creador = 'antoniojaj'

        adiciona_usuario(conn, login=creador, nome='Antonio Andraues')
        adiciona_usuario(conn, login='gabrielvf', nome='Gabriel Francato')
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO @gabrielvf @samuel",
                      titulo="teste", url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        id_post = acha_post(conn, login=creador, titulo="teste")
        lista_de_curtidas = ['antoniojaj', 'gabrielvf']

        add_curtida(conn=conn, login='gabrielvf', post_id=id_post,
                    browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        add_curtida(conn=conn, login='antoniojaj', post_id=id_post,
                    browser='safari', aparelho='MAC-os', IP='127.0.0.1')
        res = lista_curtidas(conn, id_post)
        self.assertCountEqual(res, lista_de_curtidas)

    def test_lista_user_famosos_regiao(self):
        conn = self.__class__.connection
        creador = "antoniojaj"
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', cidade="Sao Paulo")
        adiciona_usuario(conn, login='gabrielvf',
                         nome='Gabriel Francato', cidade="Sao Paulo")
        adiciona_usuario(conn, login='samuelvgb',
                         nome='Samuel', cidade="Bahia")
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO @gabrielvf @antoniojaj",
                      titulo="teste", url="NULL", estado="Ativo")
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO!!! @gabrielvf @samuelvgb",
                      titulo="testando", url="NULL", estado="Ativo")
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO @gabrielvf",
                      titulo="teste", url="NULL", estado="Ativo")
        resultado = lista_user_pop_cidade(conn)
        resultado_deve_ser = [
            ('Sao Paulo', 3, 'gabrielvf'), ('Bahia', 1, 'samuelvgb')]
        self.assertListEqual(resultado, resultado_deve_ser)

    def test_lista_post_cron_rev(self):
        conn = self.__class__.connection
        creador = "antoniojaj"
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', cidade="Sao Paulo")
        adiciona_usuario(conn, login='gabrielvf',
                         nome='Gabriel Francato', cidade="Sao Paulo")
        adiciona_post(conn, login=creador, texto="Legal demais", titulo="Top", url="NULL", estado="Ativo",
                      date='2015-11-05 14:29:36', browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        adiciona_post(conn=conn, login=creador, texto="Top Demais", titulo="Legal", url="NULL",
                      estado="Ativo", date='2019-11-05 14:29:36', browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        resultado = lista_post_cron_reverso(conn)
        date_time_str = resultado[0][6]
        date_time_str1 = resultado[1][6]
        self.assertGreater(date_time_str, date_time_str1)

    def test_lista_usr_from_refs(self):
        conn = self.__class__.connection
        creador = "antoniojaj"
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', cidade="Sao Paulo")
        adiciona_usuario(conn, login='gabrielvf',
                         nome='Gabriel Francato', cidade="Sao Paulo")
        adiciona_usuario(conn, login='samuelgranato',
                         nome='Gabriel Francato', cidade="Sao Paulo")
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO @gabrielvf @antoniojaj",
                      titulo="teste", url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO @gabrielvf", titulo="teste",
                      url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        adiciona_post(conn=conn, login='samuelgranato', texto="DEMAIS ESSE PASSARO @gabrielvf",
                      titulo="teste", url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        res = lista_usr_from_refs(conn, 'gabrielvf')
        referencias_gabrielvf = ["antoniojaj", "samuelgranato"]
        self.assertCountEqual(res, referencias_gabrielvf)
        self.assertListEqual(list(res), referencias_gabrielvf)

    def test_adiciona_tipo_acao(self):
        conn = self.__class__.connection
        acoes = ["Get", "Post", "Visualizacao"]
        for a in acoes:
            adiciona_tipo_acao(conn, a)
        res = lista_tipo_acoes(conn)
        self.assertCountEqual(res, acoes)
        self.assertListEqual(list(res), acoes)

    def test_adiciona_acao(self):
        conn = self.__class__.connection
        creador = "antoniojaj"
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', cidade="Sao Paulo")
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO ", titulo="teste",
                      url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        post_id = acha_post(conn, creador, "teste")
        add_curtida(conn, login=creador, post_id=post_id,
                    browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        acoes = lista_tipo_acoes(conn)
        self.assertIn('adiciona_post', acoes)
        self.assertIn('curtir', acoes)

    def test_tabela_browser_aparelho(self):
        conn = self.__class__.connection
        creador = "antoniojaj"
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', cidade="Sao Paulo")
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO ", titulo="teste",
                      url="NULL", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        post_id = acha_post(conn, creador, "teste")
        add_curtida(conn, login=creador, post_id=post_id,
                    browser='safari', aparelho='MAC-os', IP='127.0.0.0')
        add_curtida(conn, login=creador, post_id=post_id,
                    browser='chrome', aparelho='IOS', IP='127.0.0.0')
        add_curtida(conn, login=creador, post_id=post_id,
                    browser='IE', aparelho='Windows', IP='127.0.0.0')
        tabela = quantidade_aparelho_browser(conn)
        resultado_deve_ser = [
            ('safari', 'MAC-os', 2), ('chrome', 'IOS', 1), ('IE', 'Windows', 1)]
        self.assertListEqual(tabela, resultado_deve_ser)

    def test_url_passaro(self):
        conn = self.__class__.connection

        titulo = "teste passaro ref"
        creador = 'antoniojaj'
        adiciona_usuario(conn, login=creador,
                         nome='Antonio Andraues', email="teste@a.com")
        passaro = 'canario da terra'

        # Adiciona um passaro não existente.
        adiciona_passaro(conn, passaro)
        adiciona_passaro(conn, "cacatua")
        # Adiciona um post
        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO #canario", titulo=titulo,
                      url="www.canario.com.br", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')

        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO #canario", titulo="oi",
                      url="www.canariolindo.com.br", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')

        adiciona_post(conn=conn, login=creador, texto="DEMAIS ESSE PASSARO #cacatua", titulo="123",
                      url="www.cacatua.com.br", estado="Ativo", browser='safari', aparelho='MAC-os', IP='127.0.0.0')


        res = list_url_passaro(conn)
        resultado_deve_ser = [
            ('www.canario.com.br', 'canario da terra'), ('www.canariolindo.com.br', 'canario da terra'), ('www.cacatua.com.br', 'cacatua')]
        self.assertListEqual(list(res), resultado_deve_ser)


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
