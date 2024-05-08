from flask import Blueprint, render_template, request
from routes.banco_bp import execute_query

movimentacoes_bp = Blueprint('movimentacoes_bp', __name__, url_prefix='/adm')

@movimentacoes_bp.route('/movimentacoes', methods=['GET', 'POST'])
def movimentacoes():
    if request.method == 'POST':
        tipo_movimentacao = request.form.get('movimentacao')

        # Verificar o tipo de movimentação selecionado
        if tipo_movimentacao == 'todos':
            # Se 'todos' for selecionado, recuperar todas as movimentações
            movimentacoes = execute_query("SELECT * FROM movimentacoes_estoque")
        elif tipo_movimentacao == 'produtos':
            # Se 'produtos' for selecionado, recuperar movimentações filtradas por produto
            produto_selecionado = request.form.get('produto')
            if produto_selecionado:
                query = """
                    SELECT me.*, p.nome AS nome_produto
                    FROM movimentacoes_estoque AS me
                    LEFT JOIN produtos AS p ON me.produto_id = p.id
                    WHERE me.produto_id = %s
                """
                movimentacoes = execute_query(query, (produto_selecionado,))
            else:
                movimentacoes = execute_query("SELECT * FROM movimentacoes_estoque")
        elif tipo_movimentacao == 'funcionarios':
            # Se 'funcionarios' for selecionado, recuperar movimentações filtradas por funcionário
            funcionario_selecionado = request.form.get('funcionario')
            if funcionario_selecionado:
                query = """
                    SELECT me.*, f.nome AS nome_funcionario
                    FROM movimentacoes_estoque AS me
                    LEFT JOIN funcionarios AS f ON me.funcionario_id = f.id
                    WHERE me.funcionario_id = %s
                """
                movimentacoes = execute_query(query, (funcionario_selecionado,))
            else:
                movimentacoes = execute_query("SELECT * FROM movimentacoes_estoque")
        else:
            # Se nenhum tipo de movimentação for selecionado, retornar todas as movimentações
            movimentacoes = execute_query("SELECT * FROM movimentacoes_estoque")

        return render_template('adm/movimentacoes.html', movimentacoes=movimentacoes)
    else:
        # Se for um GET, apenas renderize a página com a seleção do tipo de movimentação
        return render_template('adm/movimentacoes.html')
