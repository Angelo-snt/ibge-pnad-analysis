# preparar_dados_powerbi.py - SEM EMOJIS
import pandas as pd
import sqlite3

def criar_tabela_powerbi():
    """Cria tabela otimizada para Power BI"""
    
    # Caminho correto para o banco
    conn = sqlite3.connect('../data/ibge_analise.db')
    
    try:
        # Ler dados historicos
        df = pd.read_sql("SELECT * FROM pnad_historico", conn)
        
        if df.empty:
            print("Nenhum dado encontrado")
            return
        
        # TRATAMENTO PARA POWER BI
        df_powerbi = df.copy()
        
        # 1. Renomear colunas para PT-BR
        mapeamento_colunas = {
            'V': 'taxa_desocupacao',
            'D1N': 'localidade', 
            'D2N': 'indicador',
            'D3N': 'periodo',
            'MC': 'unidade_medida',
            'MN': 'unidade'
        }
        df_powerbi = df_powerbi.rename(columns=mapeamento_colunas)
        
        # 2. Converter tipos
        df_powerbi['taxa_desocupacao'] = pd.to_numeric(df_powerbi['taxa_desocupacao'], errors='coerce')
        
        # 3. Extrair ano e trimestre do periodo
        df_powerbi['ano'] = df_powerbi['periodo'].str.extract(r'(\d{4})')
        df_powerbi['trimestre'] = df_powerbi['periodo'].str.extract(r'(\w{3}-\w{3}-\w{3})')
        
        # 4. Ordenar por periodo
        df_powerbi = df_powerbi.sort_values('periodo')
        
        # 5. Calcular variacao periodica
        df_powerbi['variacao_periodo'] = df_powerbi['taxa_desocupacao'].pct_change() * 100
        
        # Salvar tabela otimizada
        df_powerbi.to_sql('powerbi_otimizado', conn, if_exists='replace', index=False)
        
        # Tambem salvar como CSV
        df_powerbi.to_csv('../data/dados_powerbi_otimizado.csv', index=False, encoding='utf-8')
        
        print("Tabela Power BI criada com sucesso!")
        print(f"Colunas: {list(df_powerbi.columns)}")
        print(f"Periodos: {df_powerbi['periodo'].nunique()}")
        print(f"Registros: {len(df_powerbi)}")
        
        # Mostrar preview
        print("Preview dos dados:")
        print(df_powerbi[['periodo', 'taxa_desocupacao', 'variacao_periodo']].head())
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    criar_tabela_powerbi()