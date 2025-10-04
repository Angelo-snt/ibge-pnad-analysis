# verificar_dados.py
import sqlite3
import pandas as pd

def verificar_banco():
    print("Verificando banco de dados...")
    
    try:
        # Conecta ao banco
        conn = sqlite3.connect('ibge_analise.db')
        
        # Lista todas as tabelas
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        
        print(f"Tabelas no banco: {tabelas}")
        
        # Mostra dados de cada tabela
        for tabela in tabelas:
            nome_tabela = tabela[0]
            print(f"\n--- Dados da tabela: {nome_tabela} ---")
            
            # Conta registros
            cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela}")
            total = cursor.fetchone()[0]
            print(f"Total de registros: {total}")
            
            # Mostra primeiras linhas
            if total > 0:
                df = pd.read_sql(f"SELECT * FROM {nome_tabela} LIMIT 3", conn)
                print(df)
        
        conn.close()
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    verificar_banco()