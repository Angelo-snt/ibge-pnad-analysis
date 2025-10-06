# verificar_dados.py
import pandas as pd
import sqlite3

def verificar_dashboard():
    print(" VERIFICANDO DADOS DO DASHBOARD...")
    
    conn = sqlite3.connect('../data/ibge_analise.db')
    
    try:
        # Ler dados da tabela dashboard_pnad
        df = pd.read_sql('SELECT * FROM dashboard_pnad', conn)
        
        print(f" Total de registros: {len(df)}")
        print(f" Anos únicos: {sorted(df['ano'].unique())}")
        
        print("\n Períodos por ano:")
        print(df.groupby('ano').size())
        
        print("\n Primeiras linhas:")
        print(df[['periodo', 'ano', 'trimestre', 'taxa_desocupacao']].head(10))
        
        print(f"\n Taxa mais recente: {df['taxa_desocupacao'].iloc[-1]:.2f}%")
        print(f" Média histórica: {df['taxa_desocupacao'].mean():.2f}%")
        
    except Exception as e:
        print(f" Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_dashboard()