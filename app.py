#Arquivo que será usando para desenvolver APIRest em flask

from flask import Flask
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'database/db.sqlite3'

def executar_script_sql(conn, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        conn.executescript(sql_script)

@app.route('/')
def iniciar_database():
    try:
        # Remove o banco anterior 
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            
        # Conecta e cria o banco SQLite
        conn = sqlite3.connect(DB_PATH)

        # Cria tabelas
        executar_script_sql(conn, 'database/schema.sql')

        # Insere dados
        executar_script_sql(conn, 'database/data.sql')

        conn.commit()
        return 'Banco de dados SQLite criado e populado com sucesso!'

    except Exception as e:
        return f'Erro ao criar banco: {e}'

    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
