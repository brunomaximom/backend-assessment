import os, json, psycopg2, subprocess, requests
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
conn = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=eu")
cur = conn.cursor(cursor_factory=RealDictCursor)
access_token = None

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
    global access_token
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
    return 'Rotas diponíveis: \n/cancelar\n/solicitar\n/avaliar\n/login'

@app.route('/solicitar')
def solicitar():
    """Solicita ativação

    Returns:
        string: mensagem de sucesso.
    """
    global access_token
    if access_token == None:
        return "Usuário não autenticado"
    else:
        r = requests.get('http://localhost:5000/protected', headers="Authorization: Bearer "+access_token).content

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
    global access_token
    if access_token == None:
        return "Usuário não autenticado"
    else:
        r = requests.get('http://localhost:5000/protected', headers="Authorization: Bearer "+access_token).content
        
    id = request.args.get('id')
    out = subprocess.run(["go", "run", "consumer.go", "0", "id"], stdout=subprocess.PIPE)
    return out.stdout.decode('utf-8')

@app.route('/visualizar')
def visualizar():
    """Recuperar dado desejado do banco pelo id

    Returns:
        json: Registro desejado em formato json
    """
    global access_token
    if access_token == None:
        return "Usuário não autenticado"
    else:
        r = requests.get('http://localhost:5000/protected', headers="Authorization: Bearer "+access_token).content

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
    global access_token
    if access_token == None:
        return "Usuário não autenticado"
    else:
        r = requests.get('http://localhost:5000/protected', headers="Authorization: Bearer "+access_token).content

    if r['logged_in_as'] == 'usuario1':         #usuario1 é o super-usuário
        opcode = request.args.get('opcode')
        id = request.args.get('id')
        out = subprocess.run(["go", "run", "consumer.go", opcode, "id"], stdout=subprocess.PIPE)
        print(out.stdout.decode('utf-8'))

        if opcode == '1':
            return "Ativação recusada pelo super usuário"
        elif opcode == '2':
            return "Ativação aprovada pelo super usuário"
        else:
            return "Um erro ocorreu. Conferir se foi passado o opcode correto."
    else:
        return "Voce não é super-usuário"