from flask import Blueprint, render_template, request, redirect, url_for
from routes.banco_bp import execute_query

cad_CA_bp = Blueprint('cad_CA_bp', __name__, url_prefix='/adm')

# Função para verificar se o usuário está logado como administrador
def verificar_admin():
    # Coloque aqui a lógica para verificar se o usuário está logado como administrador
    pass

# Rota para exibir o formulário de cadastro de CA
@cad_CA_bp.route('/cadastro_CA', methods=['GET'])
def cadastro_CA():
    verificar_admin()  # Verificar se o usuário está logado como administrador
    return render_template('adm/cad_CA.html')

# Rota para cadastrar uma nova CA
@cad_CA_bp.route('/cadastrar_CA', methods=['POST'])
def cadastrar_CA():
    verificar_admin()  # Verificar se o usuário está logado como administrador

    descricao = request.form['descricao']
    CA = request.form['CA']

    # Consulta para inserir a CA na tabela
    query = "INSERT INTO CA (descricao,CA) VALUES (%s,%s)"
    execute_query(query, (descricao,CA))

    # Redireciona de volta para a página de cadastro de CA após o cadastro
    return redirect(url_for('cad_CA_bp.cadastro_CA'))
