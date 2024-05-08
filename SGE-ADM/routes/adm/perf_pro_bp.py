from flask import Blueprint, render_template, redirect, url_for, request
from routes.banco_bp import execute_query

perf_pro_bp = Blueprint('perf_pro_bp', __name__, url_prefix='/adm')

@perf_pro_bp.route('/detalhes_produto', methods=['GET', 'POST'])
def detalhes_produto():
    if request.method == 'GET':
        produto_id = request.args.get('produto_id')
        if not produto_id:
            return redirect(url_for('adm_pro_bp.produtos_cadastrados'))

        query = f"SELECT * FROM produtos WHERE id = {produto_id};"
        produto = execute_query(query)
        if not produto:
            return "Produto não encontrado", 404

        # Recupera as opções para as listas suspensas
        marcas = execute_query("SELECT id, descricao FROM marca;")
        cas = execute_query("SELECT id, descricao FROM CA;")
        classes = execute_query("SELECT id, descricao FROM classe;")

        return render_template('adm/perf_pro.html', produto=produto[0], marcas=marcas, cas=cas, classes=classes)

    elif request.method == 'POST':
        if request.form['submit'] == 'Atualizar Dados':
            produto_id = request.form.get('produto_id')
            nome = request.form.get('nome')
            marca_id = request.form.get('marca_id')
            ca_id = request.form.get('ca_id')
            classe_id = request.form.get('classe_id')

            query = f"UPDATE produtos SET nome='{nome}', marca_id={marca_id}, CA_id={ca_id}, classe_id={classe_id} WHERE id={produto_id};"
            execute_query(query)

            return redirect(request.url)  # Redireciona de volta para a mesma página após a atualização

        elif request.form['submit'] == 'Salvar Alterações':
            produto_id = request.form.get('produto_id')
            return redirect(url_for('perf_pro_bp.detalhes_produto', produto_id=produto_id))

