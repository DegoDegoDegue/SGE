from flask import Flask, redirect,url_for,request
from routes.adm.adm_index_bp import adm_index_bp
from routes.adm.cad_func_bp import cad_func_bp
from routes.adm.adm_func_bp import adm_func_bp
from routes.adm.adm_usr_bp import adm_usr_bp
from routes.adm.cad_pro_bp import cad_pro_bp
from routes.adm.cad_classe_bp import cad_classe_bp
from routes.adm.cad_marca_bp import cad_marca_bp
from routes.adm.cad_CA_bp import cad_CA_bp
from routes.adm.adm_pro_bp import adm_pro_bp
from routes.adm.movimento_man_bp import movimento_man_bp
from routes.adm.movimentacoes_bp import movimentacoes_bp
from routes.adm.adm_mov_func_bp import adm_mov_func_bp
from routes.adm.adm_mov_bp import adm_mov_bp
from routes.adm.solic_epi_bp import solic_epi_bp
from routes.adm.perf_func_bp import perf_func_bp
from routes.adm.perf_pro_bp import perf_pro_bp

app = Flask(__name__)

# Registro dos blueprints
app.register_blueprint(adm_index_bp)
app.register_blueprint(cad_func_bp)
app.register_blueprint(adm_func_bp)
app.register_blueprint(adm_usr_bp)
app.register_blueprint(cad_pro_bp)
app.register_blueprint(cad_classe_bp)
app.register_blueprint(cad_marca_bp)
app.register_blueprint(cad_CA_bp)
app.register_blueprint(adm_pro_bp)
app.register_blueprint(movimento_man_bp)
app.register_blueprint(movimentacoes_bp)
app.register_blueprint(adm_mov_func_bp)
app.register_blueprint(adm_mov_bp)
app.register_blueprint(solic_epi_bp)
app.register_blueprint(perf_func_bp)
app.register_blueprint(perf_pro_bp)

# Pasta para salvar as imagens
UPLOAD_FOLDER = r'static\img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'chave'


# Rota para redirecionar para /adm
@app.route('/')
def redirect_to_adm():
    return redirect(url_for('adm_index_bp.index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')