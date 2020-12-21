import os, json, psycopg2
from flask import Flask, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

@app.route('/')
def home():
    return 'Rotas diponíveis: \n/cancelar\n/solicitar\n/avaliar'

@app.route('/solicitar')
def solicitar():
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    os.system("go run producer.go "+origem+" "+destino)
    return "Ativação solicitada com sucesso"

@app.route('/cancelar')
def cancelar():
    id = request.args.get('id')
    os.system("go run consumer.go 0 "+id)
    return "Ativação cancelada"

@app.route('/visualizar')
def visualizar():
    id = request.args.get('id')
    conn = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=eu")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM t10.ativacao WHERE id="+id+";")
    return cur.fetchone()

@app.route('/avaliar')
def avaliar():
    opcode = request.args.get('opcode')
    id = request.args.get('id')
    os.system("go run consumer.go "+opcode+" "+id)
    if opcode == 1:
        return "Ativação recusada pelo super usuário"
    if opcode == 2:
        return "Ativação aprovada pelo super usuário"