from flask import Blueprint, render_template, session, redirect, url_for, request
from routes.banco_bp import execute_query

cad_pro_bp = Blueprint('cad_pro_bp', __name__, url_prefix='/adm')

# Rota para renderizar a tela de cadastro de produto
@cad_pro_bp.route('/cadastro_produto')
def cadastro_produto():
    # Recuperar as classes existentes para preencher o campo select
    query_classe = "SELECT id, descricao FROM classe"
    classes = execute_query(query_classe)

    # Recuperar as marcas existentes para preencher o campo select
    query_marca = "SELECT id, descricao FROM marca"
    marcas = execute_query(query_marca)

    # Recuperar os CAs existentes para preencher o campo select
    query_ncm = "SELECT id, descricao FROM CA"
    ncms = execute_query(query_ncm)

    return render_template('adm/cad_pro.html', classes=classes, marcas=marcas, ncms=ncms)

# Rota para cadastrar um novo produto
@cad_pro_bp.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form['nome']
    marca_id = request.form['marca']
    ncm_id = request.form['CA']
    classe_id = request.form['classe']  

    query = "INSERT INTO produtos (nome, marca_id, CA_id, data_inclusao, classe_id, ativo) VALUES (%s, %s, %s, NOW(), %s, 'S')"
    values = (nome, marca_id, ncm_id, classe_id)
    execute_query(query, values)

    return redirect(url_for('cad_pro_bp.cadastro_produto'))


