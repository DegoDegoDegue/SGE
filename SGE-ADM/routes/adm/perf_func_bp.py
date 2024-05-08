from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from routes.banco_bp import execute_query

perf_func_bp = Blueprint('perf_func_bp', __name__, url_prefix='/perf_func')

@perf_func_bp.route('/<int:funcionario_id>')
def renderizar_pagina(funcionario_id):
    # Consulta para obter o nome do funcionário
    query_funcionario = "SELECT nome FROM funcionarios WHERE id = %s"
    funcionario = execute_query(query_funcionario, (funcionario_id,))

    if not funcionario:
        return "Funcionário não encontrado", 404

    # Consulta para obter os produtos associados ao funcionário
    query_produtos = """
        SELECT p.nome, SUM(COALESCE(m.entrada, 0)) - SUM(COALESCE(m.saida, 0)) AS quantidade
        FROM produtos p
        LEFT JOIN movimentacoes_estoque m ON p.id = m.produto_id
        WHERE m.funcionario_id = %s
        GROUP BY p.nome
        HAVING SUM(COALESCE(m.entrada, 0)) - SUM(COALESCE(m.saida, 0)) > 0
    """
    produtos = execute_query(query_produtos, (funcionario_id,))

    return render_template('adm/perf_func.html', funcionario=funcionario[0][0], produtos=produtos)

@perf_func_bp.route('/devolver_produto/<string:funcionario>/<string:produto>', methods=['POST'])
def devolver_produto(funcionario, produto):
    # Obter a quantidade de produtos a serem devolvidos do formulário
    quantidade_devolucao = int(request.form['quantidade'])

    # Consulta para obter o ID do funcionário
    query_funcionario_id = "SELECT id FROM funcionarios WHERE nome = %s"
    funcionario_id = execute_query(query_funcionario_id, (funcionario,))

    if not funcionario_id:
        return jsonify({'error': 'Funcionário não encontrado'}), 404

    funcionario_id = funcionario_id[0][0]

    # Consulta para obter o ID do produto
    query_produto_id = "SELECT id FROM produtos WHERE nome = %s"
    produto_id = execute_query(query_produto_id, (produto,))

    if not produto_id:
        return jsonify({'error': 'Produto não encontrado'}), 404

    produto_id = produto_id[0][0]

    # Verificar se o produto está disponível para devolução pelo funcionário
    query_quantidade_produto = """
        SELECT COALESCE(SUM(entrada), 0) - COALESCE(SUM(saida), 0) AS quantidade_disponivel
        FROM movimentacoes_estoque
        WHERE funcionario_id = %s AND produto_id = %s
    """
    quantidade_disponivel = execute_query(query_quantidade_produto, (funcionario_id, produto_id))

    if quantidade_disponivel[0][0] < quantidade_devolucao:
        return jsonify({'error': 'Quantidade solicitada indisponível para devolução'}), 400

    # Consulta para obter o próximo ID da movimentação de estoque
    query_proximo_id = "SELECT MAX(id) FROM movimentacoes_estoque"
    proximo_id = execute_query(query_proximo_id)[0][0] + 1 if execute_query(query_proximo_id)[0][0] else 1

    # Consulta para obter o nome do funcionário
    query_nome_funcionario = "SELECT nome FROM funcionarios WHERE id = %s"
    nome_funcionario = execute_query(query_nome_funcionario, (funcionario_id,))[0][0]

    # Concatenar o nome do funcionário à mensagem tipomov_saida
    tipomov_saida = f"SAIDA DEVOLUÇÃO - {nome_funcionario}"

    # Inserir registro de movimentação de saída para o funcionário
    query_movimentacao_saida = "INSERT INTO movimentacoes_estoque (id, produto_id, saida, tipomov, funcionario_id) VALUES (%s, %s, %s, %s, %s)"
    execute_query(query_movimentacao_saida, (proximo_id, produto_id, quantidade_devolucao, tipomov_saida, funcionario_id))

    # Inserir registro de movimentação de entrada para o usuário com ID 1
    query_movimentacao_entrada = "INSERT INTO movimentacoes_estoque (id, produto_id, entrada, tipomov, funcionario_id) VALUES (%s, %s, %s, %s, %s)"
    execute_query(query_movimentacao_entrada, (proximo_id + 1, produto_id, quantidade_devolucao, 'ENTRADA ESTOQUE - DEVOLUÇÃO', 1))

    # Redirecionar de volta para a página de detalhes do funcionário
    return redirect(url_for('perf_func_bp.renderizar_pagina', funcionario_id=funcionario_id))
