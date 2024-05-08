from flask import Flask, Blueprint, render_template, session, redirect, url_for, request
from routes.banco_bp import execute_query

cad_func_bp = Blueprint('cad_func_bp', __name__, url_prefix='/adm')

@cad_func_bp.route('/cadastro_funcionario')
def cadastro_funcionario():
    return render_template('adm/cad_func.html')

@cad_func_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        query = "INSERT INTO funcionarios (nome, senha, ativo) VALUES (%s, %s,'S')"
        params = (nome, senha)
        
        try:
            execute_query(query, params)
            # Redireciona para a página de cadastro após o sucesso do cadastro
            return redirect(url_for('cad_func_bp.cadastro_funcionario'))
        except Exception as e:
            return render_template('adm/cad_func.html', error="Erro ao cadastrar usuário. Tente novamente.")

    # Retorna um erro 405 se o método não for POST
    return abort(405)


app = Flask(__name__)

# Registro da blueprint
app.register_blueprint(cad_func_bp)

if __name__ == '__main__':
    app.run(debug=True)
