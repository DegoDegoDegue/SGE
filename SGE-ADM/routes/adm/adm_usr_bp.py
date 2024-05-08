from flask import Blueprint, render_template, request, redirect, url_for
from routes.banco_bp import execute_query

adm_usr_bp = Blueprint('adm_usr_bp', __name__, url_prefix='/adm')

@adm_usr_bp.route('/exibir_usuarios')
def exibir_usuarios():
    # Consulta ao banco de dados para obter os usuários cadastrados, excluindo o usuário com ID 1
    usuarios = execute_query("SELECT id, login FROM usuarios WHERE id != 1")
    return render_template('adm/adm_usr.html', usuarios=usuarios)

@adm_usr_bp.route('/excluir_usuario/<int:id>', methods=['POST'])
def excluir_usuario(id):
    if request.method == 'POST':
        # Verificar se o ID é diferente de 1 antes de excluir
        if id != 1:
            # Executar a exclusão do usuário com o ID fornecido
            execute_query("DELETE FROM usuarios WHERE id = %s", (id,))
        return redirect(url_for('adm_usr_bp.exibir_usuarios'))

    # Se a requisição não for POST, redirecionar de volta para a página de exibição de usuários
    return redirect(url_for('adm_usr_bp.exibir_usuarios'))
