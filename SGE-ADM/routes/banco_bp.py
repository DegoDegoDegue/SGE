import mysql.connector

# Função para conectar ao banco de dados e obter um cursor
def get_cursor():
    # Configurações do banco de dados MySQL
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'sge'
    }
    
    # Conexão com o banco de dados e obtenção de um cursor
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    return conn, cursor

# Função para executar uma consulta SQL no banco de dados
def execute_query(query, params=None):
    # Obtenha a conexão e o cursor do banco de dados
    conn, cursor = get_cursor()

    try:
        # Executa a consulta SQL com os parâmetros fornecidos
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Recupera os resultados, se houver
        results = cursor.fetchall()

        # Commit e fechar a conexão
        conn.commit()
        conn.close()

        return results
    except Exception as e:
        # Em caso de erro, faz rollback e fecha a conexão
        conn.rollback()
        conn.close()
        raise e

# Função para executar uma inserção no banco de dados
def execute_insert(query, params=None):
    # Obtenha a conexão e o cursor do banco de dados
    conn, cursor = get_cursor()

    try:
        # Executa a inserção SQL com os parâmetros fornecidos
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Commit e fechar a conexão
        conn.commit()
        conn.close()

    except Exception as e:
        # Em caso de erro, faz rollback e fecha a conexão
        conn.rollback()
        conn.close()
        raise e

# Variável de conexão exportada
conn = get_cursor()[0]
