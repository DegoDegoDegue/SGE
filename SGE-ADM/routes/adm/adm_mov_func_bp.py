from flask import Blueprint, render_template, request
from routes.banco_bp import execute_query

adm_mov_func_bp = Blueprint('adm_mov_func_bp', __name__, url_prefix='/adm')

@adm_mov_func_bp.route('/movimentos_funcionario', methods=['GET', 'POST'])
def movimentos_funcionario():
    if request.method == 'POST':
        funcionarios_selecionados = request.form.getlist('funcionarios')
        query = "SELECT * FROM movimentacoes_estoque WHERE funcionario_id IN (%s)" % ','.join(['%s'] * len(funcionarios_selecionados))
        movimentos = execute_query(query, funcionarios_selecionados)
    else:
        # Se a solicitação for um GET, apenas exiba todos os movimentos de estoque para produtos que são EPI
        query = """
            SELECT me.*
            FROM movimentacoes_estoque me
            INNER JOIN produtos p ON me.produto_id = p.id
            WHERE p.classe_id = (SELECT id FROM classe WHERE descricao = 'EPI') AND me.funcionario_id IS NOT NULL
        """
        movimentos = execute_query(query)
    
    funcionarios = execute_query("SELECT id, nome FROM funcionarios")
    
    return render_template('adm/movimento_func.html', movimentos=movimentos, funcionarios=funcionarios)
