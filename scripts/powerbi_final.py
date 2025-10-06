# powerbi_final.py - VERSÃO ATUALIZADA COM SQLITE
import pandas as pd
import sqlite3
import numpy as np
import os

def criar_dataset_powerbi():
    print("Criando dataset otimizado para Power BI...")
    
    # Caminho correto para o banco (na pasta data)
    caminho_banco = "../data/ibge_analise.db"
    
    # Verifica se o banco existe
    if not os.path.exists(caminho_banco):
        print("Erro: Banco de dados nao encontrado em:", caminho_banco)
        return None
    
    conn = sqlite3.connect(caminho_banco)
    
    try:
        # Tenta ler da tabela powerbi_otimizado
        df = pd.read_sql("SELECT * FROM powerbi_otimizado", conn)
        print("Lendo dados da tabela powerbi_otimizado...")
        
        if df.empty:
            print("Nenhum dado encontrado")
            return None
        
        # TRATAMENTO AVANCADO PARA POWER BI
        df_final = df.copy()
        
        # 1. Criar data completa para eixo temporal
        df_final['data_referencia'] = pd.to_datetime(
            df_final['periodo'].str[-4:] + '-04-01',
            errors='coerce'
        )
        
        # 2. Calcular metricas avançadas
        media_historica = df_final['taxa_desocupacao'].mean()
        df_final['vs_media_historica'] = df_final['taxa_desocupacao'] - media_historica
        df_final['status'] = df_final['vs_media_historica'].apply(
            lambda x: 'Acima da Media' if x > 0 else 'Abaixo da Media'
        )
        
        # 3. Classificar por nivel de desocupacao
        condicoes = [
            df_final['taxa_desocupacao'] <= 7,
            (df_final['taxa_desocupacao'] > 7) & (df_final['taxa_desocupacao'] <= 10),
            df_final['taxa_desocupacao'] > 10
        ]
        categorias = ['Baixa', 'Moderada', 'Alta']
        df_final['nivel_desocupacao'] = np.select(condicoes, categorias, default='Moderada')
        
        # 4. Ordenar por data
        df_final = df_final.sort_values('data_referencia')
        
        # 5. Calcular media movel (suaviza a linha)
        df_final['media_movel_4p'] = df_final['taxa_desocupacao'].rolling(window=4, min_periods=1).mean()
        
        # 6. Selecionar colunas finais
        colunas_finais = [
            'data_referencia', 'periodo', 'ano', 'trimestre',
            'taxa_desocupacao', 'variacao_periodo', 'vs_media_historica',
            'status', 'nivel_desocupacao', 'media_movel_4p', 'localidade'
        ]
        
        df_final = df_final[colunas_finais]
        
        # ========== SALVAMENTO DUPLO ==========
        
        # 1. SALVAR COMO CSV (para Power BI)
        caminho_csv = "../data/pnad_powerbi_pronto.csv"
        df_final.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
        print(" CSV criado: pnad_powerbi_pronto.csv")
        
        # 2. SALVAR NO SQLITE (tabela específica)
        nome_tabela_sql = "dashboard_pnad"
        df_final.to_sql(nome_tabela_sql, conn, if_exists='replace', index=False)
        print(f" Tabela SQLite criada: {nome_tabela_sql}")
        
        # 3. VERIFICAR TABELAS EXISTENTES
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        print(f" Tabelas no banco: {[t[0] for t in tabelas]}")
        
        # 4. VERIFICAR DADOS SALVOS
        cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela_sql}")
        count = cursor.fetchone()[0]
        print(f" Registros na tabela {nome_tabela_sql}: {count}")
        
        # ========== FIM DO SALVAMENTO ==========
        
        print(f" Total de registros processados: {len(df_final)}")
        print(f" Período: {df_final['data_referencia'].min().year} a {df_final['data_referencia'].max().year}")
        print(f" Taxa média: {df_final['taxa_desocupacao'].mean():.2f}%")
        print(" Amostra dos dados:")
        print(df_final.head(3))
        
        return df_final
        
    except Exception as e:
        print(f" Erro: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    criar_dataset_powerbi()