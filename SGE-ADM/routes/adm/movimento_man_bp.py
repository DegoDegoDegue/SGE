from flask import Blueprint, render_template, request, redirect, url_for
from routes.banco_bp import execute_query, execute_insert

movimento_man_bp = Blueprint('movimento_man_bp', __name__, url_prefix='/adm')

@movimento_man_bp.route('/movimento', methods=['GET', 'POST'])
def registrar_movimento():
    if request.method == 'POST':
        produto_id = request.form['produto']
        tipo_movimento = request.form['tipo_movimento']
        quantidade = int(request.form['quantidade'])

        if tipo_movimento == 'saida':
            pass

        elif tipo_movimento == 'descarte':
            # Insere a movimentação de estoque (saída) para o descarte do produto
            query_descarte = "INSERT INTO movimentacoes_estoque (produto_id, saida, tipomov, funcionario_id) VALUES (%s, %s, %s, %s)"
            execute_insert(query_descarte, (produto_id, quantidade, "DESCARTE", 1))
            return redirect(url_for('movimento_man_bp.registrar_movimento'))

        # Insere a movimentação de estoque no banco de dados
        if tipo_movimento == 'entrada':
            # Se for uma entrada, insere o valor na coluna "entrada" e define "saida" como 0
            query = "INSERT INTO movimentacoes_estoque (produto_id, entrada, saida, tipomov, funcionario_id) VALUES (%s, %s, %s, %s, %s)"
            values = (produto_id, quantidade, 0, "MOVIMENTO MANUAL - ENTRADA", 1)
        else:
            # Se for uma saída, insere o valor na coluna "saida" e define "entrada" como 0
            query = "INSERT INTO movimentacoes_estoque (produto_id, entrada, saida, tipomov, funcionario_id) VALUES (%s, %s, %s, %s, %s)"
            values = (produto_id, 0, quantidade, "MOVIMENTO MANUAL - SAIDA", 1)
        
        execute_insert(query, values)

        # Redireciona para a página inicial ou para onde você deseja após o registro
        return redirect(url_for('movimento_man_bp.registrar_movimento'))

    # Se o método for GET, renderiza o template do formulário
    produtos = execute_query("SELECT id, nome FROM produtos")
    return render_template('adm/movimento_man.html', produtos=produtos)
