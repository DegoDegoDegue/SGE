from flask import Blueprint, render_template, request, redirect, url_for
from routes.banco_bp import execute_query

adm_mov_bp = Blueprint('adm_mov_bp', __name__, url_prefix='/adm')

@adm_mov_bp.route('/verificar_movimentos', methods=['GET', 'POST'])
def verificar_movimentos():
    if request.method == 'POST':
        # Se a solicitação for um POST, significa que o usuário enviou uma seleção de produtos
        produtos_selecionados = request.form.getlist('produtos')  # Obter a lista de produtos selecionados
        # Consulta SQL para obter os movimentos de estoque apenas para os produtos selecionados
        query = """SELECT m.*, p.nome 
           FROM movimentacoes_estoque m 
           LEFT JOIN produtos p ON m.produto_id = p.id 
           WHERE m.produto_id IN (%s)""" % ','.join(['%s'] * len(produtos_selecionados))

        movimentos = execute_query(query, produtos_selecionados)
    else:
        # Se a solicitação for um GET, apenas exiba todos os movimentos de estoque
        movimentos = execute_query("""SELECT m.id, m.produto_id, m.entrada, m.saida, m.data_movimentacao, m.tipomov, m.solicitacao_id, m.funcionario_id, p.nome
                                      FROM movimentacoes_estoque m
                                      LEFT JOIN produtos p ON m.produto_id = p.id""")
    
    # Consulta para obter todos os produtos para exibir na seleção
    produtos = execute_query("SELECT id, nome FROM produtos")
    
    return render_template('adm/adm_mov.html', movimentos=movimentos, produtos=produtos)
