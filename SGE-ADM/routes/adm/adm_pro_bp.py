from flask import Blueprint, render_template, session, redirect, url_for, request
from routes.banco_bp import execute_query

adm_pro_bp = Blueprint('adm_pro_bp', __name__, url_prefix='/adm')

# Rota para exibir os produtos cadastrados
@adm_pro_bp.route('/produtos_cadastrados')
def produtos_cadastrados():
    # Consulta SQL para recuperar os produtos e o estoque atual
    query = """
    SELECT p.id, p.nome, e.quantidade, c.descricao, m.descricao, ca.CA
    FROM produtos p
    LEFT JOIN estoque e ON p.id = e.produto_id
    LEFT JOIN classe c ON p.classe_id = c.id
    LEFT JOIN marca m ON p.marca_id = c.id
    LEFT JOIN CA ca ON p.CA_id = ca.id
"""

    # Executar a consulta
    produtos = execute_query(query)

    return render_template('adm/adm_pro.html', produtos=produtos)
