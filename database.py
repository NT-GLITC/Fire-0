import sqlite3

def criar_banco():
    conexao = sqlite3.connect('alertas.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conexao.commit()
    conexao.close()

def salvar_email(email):
    try:
        conexao = sqlite3.connect('alertas.db')
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO usuarios (email) VALUES (?)', (email,))
        conexao.commit()
        conexao.close()
        return True
    except:
        return False