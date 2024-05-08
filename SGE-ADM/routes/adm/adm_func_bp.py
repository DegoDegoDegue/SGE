from flask import Blueprint, render_template, redirect, url_for, request
from routes.banco_bp import execute_query

adm_func_bp = Blueprint('adm_func_bp', __name__, url_prefix='/adm')

@adm_func_bp.route('/funcionarios/inativar/<int:funcionario_id>', methods=['POST'])
def inativar_funcionario(funcionario_id):
    if request.method == 'POST':
        # Consulta para verificar a quantidade de estoque atrelado ao funcionário
        query_quantidade_produto = """
            SELECT COALESCE(SUM(entrada), 0) - COALESCE(SUM(saida), 0) AS quantidade_disponivel
            FROM movimentacoes_estoque
            WHERE funcionario_id = %s
        """
        quantidade_estoque = execute_query(query_quantidade_produto, (funcionario_id,))
        
        # Se a quantidade de estoque for maior que 0, retorna para a página de funcionários com a mensagem de erro
        if quantidade_estoque[0][0] > 0:
            mensagem = "Erro: Não é possível inativar o funcionário porque existe estoque associado a ele."
            # Consulta para obter os dados da tabela de funcionários ativos
            query_ativos = "SELECT id, nome FROM funcionarios WHERE id <> 1 AND ativo='S'"
            funcionarios_ativos = execute_query(query_ativos)
            # Consulta para obter os dados da tabela de funcionários inativos
            query_inativos = "SELECT id, nome FROM funcionarios WHERE id <> 1 AND ativo='N'"
            funcionarios_inativos = execute_query(query_inativos)
            return render_template('adm/adm_func.html', mensagem=mensagem, funcionarios_ativos=funcionarios_ativos, funcionarios_inativos=funcionarios_inativos)

        # Se não houver estoque atrelado, inativa o funcionário do banco de dados
        query = "UPDATE funcionarios SET ativo='N' WHERE id = %s"
        execute_query(query, (funcionario_id,))

        # Redireciona de volta para a página de exibição de funcionários após a inativação
        return redirect(url_for('adm_func_bp.exibir_funcionarios'))

@adm_func_bp.route('/funcionarios/ativar/<int:funcionario_id>', methods=['POST'])
def ativar_funcionario(funcionario_id):
    if request.method == 'POST':
        # Ativa o funcionário no banco de dados
        query = "UPDATE funcionarios SET ativo='S' WHERE id = %s"
        execute_query(query, (funcionario_id,))

        # Redireciona de volta para a página de exibição de funcionários após a ativação
        return redirect(url_for('adm_func_bp.exibir_funcionarios'))

# Rota para exibir os dados dos funcionários
@adm_func_bp.route('/funcionarios')
def exibir_funcionarios():

    # Consulta para obter os dados da tabela de funcionários ativos
    query_ativos = "SELECT id, nome FROM funcionarios WHERE id <> 1 AND ativo='S'"
    funcionarios_ativos = execute_query(query_ativos)

    # Consulta para obter os dados da tabela de funcionários inativos
    query_inativos = "SELECT id, nome FROM funcionarios WHERE id <> 1 AND ativo='N'"
    funcionarios_inativos = execute_query(query_inativos)

    return render_template('adm/adm_func.html', funcionarios_ativos=funcionarios_ativos, funcionarios_inativos=funcionarios_inativos)
