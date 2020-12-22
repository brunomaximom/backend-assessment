import os, json, psycopg2
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
conn = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=eu")
cur = conn.cursor(cursor_factory=RealDictCursor)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['GET'])
def login():
    """Realiza a autenticação. Funciona com /login?username=<usuario>&password=<senha>.

    Returns:
        json: retorna um token
    """
    global cur
    usuario = request.args.get('username')
    senha = request.args.get('password')
    cur.execute("SELECT nome FROM t10.usuario WHERE nome = %s", (usuario,))
    usuario_existe = cur.fetchone()
    cur.execute("SELECT senha FROM t10.usuario WHERE senha = %s", (senha,))
    senha_existe = cur.fetchone()
    if not usuario:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not senha:
        return jsonify({"msg": "Missing password parameter"}), 400

    if usuario_existe == None or senha_existe == None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=usuario)
    return jsonify(access_token=access_token), 200

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/')
def home():
    return 'Rotas diponíveis: \n/cancelar\n/solicitar\n/avaliar'

@app.route('/solicitar')
def solicitar():
    """Solicita ativação

    Returns:
        string: mensagem de sucesso.
    """
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    os.system("go run producer.go "+origem+" "+destino)
    return "Ativação solicitada com sucesso"

@app.route('/cancelar')
def cancelar():
    """O usuário cancela a ativação

    Returns:
        string: Mensagem de evento realizado
    """
    id = request.args.get('id')
    os.system("go run consumer.go 0 "+id)
    return "Ativação cancelada"

@app.route('/visualizar')
def visualizar():
    """Recuperar dado desejado do banco pelo id

    Returns:
        json: Registro desejado em formato json
    """
    id = request.args.get('id')
    global cur
    cur.execute("SELECT * FROM t10.ativacao WHERE id="+id+";")
    return jsonify(cur.fetchone())

@app.route('/avaliar')
def avaliar():
    """Super-usuário recusa/aprova solicitação

    Returns:
        string: Retorna mensagem de recusada ou aprovada a solicitação
    """
    opcode = request.args.get('opcode')
    id = request.args.get('id')
    os.system("go run consumer.go "+opcode+" "+id)
    if opcode == 1:
        return "Ativação recusada pelo super usuário"
    if opcode == 2:
        return "Ativação aprovada pelo super usuário"