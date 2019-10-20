from fastapi import FastAPI,Header
import uvicorn
from projeto import *
import pymysql
import json

with open('config_tests.json', 'r') as f:
    config = json.load(f)
conn = pymysql.connect(
        host=config['HOST'],
        user=config['USER'],
        password=config['PASS'],
        database='mydb'
    )
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/signup/{login,nome,email,cidade}")
def read_item(login:str, nome:str, email:str, cidade:str):
    try:
        adiciona_usuario(conn,login,nome,email,cidade)
        return {"status": 200,"login":login,"nome":nome,"email":email,"cidade":cidade}
    except Exception as e:
        
        return {"status":str(e)}

@app.put("/change_email/{login,novo_email}")
def read_item(login,novo_email):
        try:
            muda_email_usuario(login,novo_email)
            return {"status": 200,"novo email":novo_email}

        except Exception as e:
            return {"status":str(e)}

@app.delete("/remove_user/{login}")
def read_item(login: str):
    try:
        remove_usuario(conn,login)
        return {"status":200,"login": login}
    except Exception as e:
        return {"status":str(e)}

@app.post("/add_pass/{nome,cor,comida,onde_vive,tamanho}")
def read_item(nome:str, cor:str = None,comida:str = None,onde_vive:str = None,tamanho:str = None):
    try:
        adiciona_passaro(conn,nome,cor,comida,onde_vive,tamanho)
        return {"status": 200}
    except Exception as e:
        return {"status":str(e)}

@app.get("/get_pass/{nome}")
def read_item(nome):
        try:
            res=acha_passaro(nome)
            return {"status": 200,"info_passaro":res}

        except Exception as e:
            return {"status":str(e)}

@app.delete("/remove_pass/{nome}")
def read_item(nome: str):
    try:
        remove_passaro(conn,nome)
        return {"status":200,"nome_passaro_removido": nome}
    except Exception as e:
        return {"status":str(e)}

@app.get("/find_usr/{login}")
def read_item(login: str):
    try:
        usr=acha_usuario(conn,login)
        return {"status": 200,"usr":usr}
    except Exception as e:
        return {"status":str(e)}

@app.get("/find_pass/{nome}")
def read_item(nome: str):
    try:
        passaro=acha_passaro(conn,nome)
        return {"status": 200,"passaro":passaro}
    except Exception as e:
        return {"status":str(e)}

@app.get("/list_pass")
def read_item():
    try:
        passaros=lista_passaros(conn)
        return {"status": 200,"lista_passaros":passaros}
    except Exception as e:

        return {"status":str(e)}

@app.get("/list_users")
def read_item():
    try:
        usuarios=lista_usuarios(conn)
        return {"status": 200,"lista_usuarios":usuarios}
    except Exception as e:

        return {"status":str(e)}

@app.get("/list_post")
def read_item():
    try:
        posts=lista_post_cron_reverso(conn)
        return {"status": 200,"posts_cronologica_reverso":posts}
    except Exception as e:

        return {"status":str(e)}

@app.delete("/remove_post/{login,postid}")
def read_item(login:str,postid:int):
    try:
        remove_post(conn,login,postid)
        return {"status": 200,"post_deletado":postid}
    except Exception as e:
        return {"status":str(e)}
@app.post("/add_post/{login,texto,titulo,url,estado}")
def read_item(*, user_agent: str = Header(None), login: str,texto:str = None, titulo: str, url: str = None, estado:str = "Ativo", date: str = "NULL"):
    try:
        adiciona_post(conn,login,texto,titulo,url,estado,date,user_agent[-1:-15],user_agent[-1:-15],user_agent[-1:-15])
        return {"status": 200}
    except Exception as e:
        return {"status":str(e), "headers": user_agent[-1:-15]}

@app.get("/lista_post_ref_pass/{idPost}")
def read_item(idPost: int):
    try:
        passaro = lista_post_ref_pass(conn,idPost)
        return {"status": 200, "passaro": passaro}
    except Exception as e:
        return {"status":str(e)}

@app.get("/lista_post_ref_usr/{idPost}")
def read_item(idPost: int):
    try:
        users = lista_post_ref_user(conn,idPost)
        return {"status": 200, "users": users}
    except Exception as e:
        return {"status":str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")

# "headers": user_agent
# *, user_agent: str = Header(None)
