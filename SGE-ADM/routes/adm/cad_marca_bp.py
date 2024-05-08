from flask import Blueprint, render_template, request, redirect, url_for
from routes.banco_bp import execute_query

cad_marca_bp = Blueprint('cad_marca_bp', __name__, url_prefix='/adm')

# Função para verificar se o usuário está logado como administrador
def verificar_admin():
    # Coloque aqui a lógica para verificar se o usuário está logado como administrador
    pass

# Rota para exibir o formulário de cadastro de marca
@cad_marca_bp.route('/cadastro_marca', methods=['GET'])
def cadastro_marca():
    verificar_admin()  # Verificar se o usuário está logado como administrador
    return render_template('adm/cad_marca.html')

# Rota para cadastrar uma nova marca
@cad_marca_bp.route('/cadastrar_marca', methods=['POST'])
def cadastrar_marca():
    verificar_admin()  # Verificar se o usuário está logado como administrador

    descricao = request.form['descricao']

    # Consulta para inserir a marca na tabela
    query = "INSERT INTO marca (descricao) VALUES (%s)"
    execute_query(query, (descricao,))

    # Redireciona de volta para a página de cadastro de marca após o cadastro
    return redirect(url_for('cad_marca_bp.cadastro_marca'))
