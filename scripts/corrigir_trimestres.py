# corrigir_trimestres.py
import pandas as pd
import sqlite3

def corrigir_dados():
    print(" CORRIGINDO DADOS PARA TRIMESTRES PADRÃO...")
    
    conn = sqlite3.connect('../data/ibge_analise.db')
    
    try:
        # Ler dados
        df = pd.read_sql('SELECT * FROM powerbi_otimizado', conn)
        
        # Manter apenas trimestres padrão
        trimestres_validos = ['jan-fev-mar', 'abr-mai-jun', 'jul-ago-set', 'out-nov-dez']
        df_corrigido = df[df['trimestre'].isin(trimestres_validos)].copy()
        
        print(f" Registros antes: {len(df)}")
        print(f" Registros depois: {len(df_corrigido)}")
        
        # Salvar tabela corrigida
        df_corrigido.to_sql('dashboard_pnad_corrigido', conn, if_exists='replace', index=False)
        print(" Tabela corrigida salva: dashboard_pnad_corrigido")
        
        # Verificar resultado
        print("\n Períodos por ano (CORRIGIDO):")
        print(df_corrigido.groupby('ano').size())
        
    except Exception as e:
        print(f" Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    corrigir_dados()