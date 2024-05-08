from flask import Blueprint, render_template, redirect, url_for, request
from datetime import datetime
from routes.banco_bp import execute_query, execute_insert, conn

solic_epi_bp = Blueprint('solic_epi_bp', __name__, url_prefix='/solic')

def execute_insert_return_id(query, data):
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")  # Assume que você está usando MySQL
    last_id = cursor.fetchone()[0]
    cursor.close()
    return last_id

def check_stock(product_id, quantity):
    query_stock = "SELECT quantidade FROM estoque WHERE produto_id = %s"
    result = execute_query(query_stock, (product_id,))
    current_stock = result[0][0]  # Acessa o primeiro elemento da primeira tupla
    return current_stock - quantity >= 0



@solic_epi_bp.route('/nova_solicitacao', methods=['GET', 'POST'])
def nova_solicitacao():
    if request.method == 'POST':
        # Captura os dados do formulário
        funcionario_id = request.form['funcionario']
        produto_id = request.form['produto']
        quantidade = int(request.form['quantidade'])

        # Verifica se o estoque do produto ficará menor que 0 após a operação
        if not check_stock(produto_id, quantidade):
            return "Operação não permitida: estoque insuficiente."

        # Insere um registro na tabela de solicitações
        query_solicitacao = "INSERT INTO solicitacoes (funcionario_id, data_solicitacao) VALUES (%s, %s)"
        data_solicitacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        solicitacao_id = execute_insert_return_id(query_solicitacao, (funcionario_id, data_solicitacao))
        
        # Consulta o nome do funcionário
        query_nome_funcionario = "SELECT nome FROM funcionarios WHERE id = %s"
        nome_funcionario = execute_query(query_nome_funcionario, (funcionario_id,))[0][0]
        
        # Adiciona o nome do funcionário à mensagem tipomov_entrada
        tipomov_entrada = f"SOLICITACAO EPI - {nome_funcionario}"
        
        # Insere um registro na tabela de movimentações de estoque (entrada)
        query_movimentacao_entrada = "INSERT INTO movimentacoes_estoque (produto_id, entrada, data_movimentacao, tipomov, solicitacao_id, funcionario_id) VALUES (%s, %s, %s, %s, %s, %s)"
        execute_insert(query_movimentacao_entrada, (produto_id, quantidade, data_solicitacao, tipomov_entrada, solicitacao_id, funcionario_id))

        # Insere um registro na tabela de movimentações de estoque (saída) para o usuário com id 1
        query_movimentacao_saida = "INSERT INTO movimentacoes_estoque (produto_id, saida, data_movimentacao, tipomov, solicitacao_id, funcionario_id) VALUES (%s, %s, %s, %s, %s, %s)"
        tipomov_saida = "SAIDA ESTOQUE"
        execute_insert(query_movimentacao_saida, (produto_id, quantidade, data_solicitacao, tipomov_saida, solicitacao_id, 1))

        return redirect(url_for('solic_epi_bp.nova_solicitacao'))  # Redireciona para a mesma página após o envio

    else:
        # Consulta os produtos no banco de dados que estão com a classe "EPI"
        query_produtos = "SELECT id, nome FROM produtos WHERE classe_id = (SELECT id FROM classe WHERE descricao = 'EPI' and ativo='S')"
        produtos = execute_query(query_produtos)

        # Consulta os funcionários no banco de dados
        query_funcionarios = "SELECT id, nome FROM funcionarios WHERE id != 1 and ativo='S'"
        funcionarios = execute_query(query_funcionarios)

        return render_template('adm/solic_epi.html', funcionarios=funcionarios, produtos=produtos)

