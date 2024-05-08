from flask import Flask, Blueprint, render_template, session, redirect, url_for, request
from routes.banco_bp import execute_query

cad_usr_bp = Blueprint('cad_usr_bp', __name__, url_prefix='/adm')

@cad_usr_bp.route('/cadastro_usuario')
def cadastro_usuario():
    return render_template('adm/cad_usr.html')

@cad_usr_bp.route('/Cadastrar_usr', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        
        query = "INSERT INTO usuarios (login, senha) VALUES (%s, %s)"
        params = (login, senha)
        
        try:
            execute_query(query, params)
            return redirect(url_for('cad_usr_bp.cadastro_usuario'))
        except Exception as e:
            return render_template('adm/cad_usr.html', error="Erro ao cadastrar usuário. Tente novamente.")

app = Flask(__name__)

# Registro da blueprint
app.register_blueprint(cad_usr_bp)

if __name__ == '__main__':
    app.run(debug=True)
