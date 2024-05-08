from flask import Blueprint, render_template
from routes.banco_bp import execute_query

adm_index_bp = Blueprint('adm_index_bp', __name__, url_prefix='/adm')

@adm_index_bp.route('/')
def index():
    # Consulta para obter os produtos e suas quantidades em estoque
    query = """
    SELECT p.nome, e.quantidade, p.classe_id
    FROM produtos p
    LEFT JOIN estoque e ON p.id = e.produto_id
    WHERE p.classe_id = 1 AND e.quantidade <=2
    """

    produtos = execute_query(query)

    # Verificar os resultados da consulta
    print(produtos)

    # Retorna o template HTML passando os dados dos produtos
    return render_template('adm/index_adm.html', produtos=produtos)
