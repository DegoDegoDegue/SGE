from flask import Blueprint, render_template, request, redirect, url_for
from routes.banco_bp import execute_query

cad_classe_bp = Blueprint('cad_classe_bp', __name__, url_prefix='/adm')

# Função para verificar se o usuário está logado como administrador
def verificar_admin():
    # Coloque aqui a lógica para verificar se o usuário está logado como administrador
    pass

# Rota para exibir o formulário de cadastro de classe
@cad_classe_bp.route('/cadastro_classe', methods=['GET'])
def cadastro_classe():
    verificar_admin()  # Verificar se o usuário está logado como administrador
    return render_template('adm/cad_classe.html')

# Rota para cadastrar uma nova classe
@cad_classe_bp.route('/cadastrar_classe', methods=['POST'])
def cadastrar_classe():
    verificar_admin()  # Verificar se o usuário está logado como administrador

    descricao = request.form['descricao']

    # Consulta para inserir a classe na tabela
    query = "INSERT INTO classe (descricao) VALUES (%s)"
    execute_query(query, (descricao,))

    # Redireciona de volta para a página de cadastro de classe após o cadastro
    return redirect(url_for('cad_classe_bp.cadastro_classe'))
