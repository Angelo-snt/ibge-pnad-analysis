# powerbi_final.py
import pandas as pd
import sqlite3
from datetime import datetime

def criar_dataset_powerbi():
    print("Criando dataset otimizado para Power BI...")
    
    conn = sqlite3.connect('ibge_analise.db')
    
    try:
        # Ler dados da tabela powerbi_otimizado
        df = pd.read_sql("SELECT * FROM powerbi_otimizado", conn)
        
        # TRATAMENTO AVANÇADO PARA POWER BI
        df_final = df.copy()
        
        # 1. Criar data completa para eixo temporal
        # Converte "abr-mai-jun 2023" para data
        df_final['data_referencia'] = pd.to_datetime(
            df_final['periodo'].str[-4:] + '-04-01',  # Usa abril como mês base
            errors='coerce'
        )
        
        # 2. Calcular métricas avançadas
        media_historica = df_final['taxa_desocupacao'].mean()
        df_final['vs_media_historica'] = df_final['taxa_desocupacao'] - media_historica
        df_final['status'] = df_final['vs_media_historica'].apply(
            lambda x: 'Acima da Média' if x > 0 else 'Abaixo da Média'
        )
        
        # 3. Classificar por nível de desocupação
        condicoes = [
            df_final['taxa_desocupacao'] <= 7,
            (df_final['taxa_desocupacao'] > 7) & (df_final['taxa_desocupacao'] <= 10),
            df_final['taxa_desocupacao'] > 10
        ]
        categorias = ['Baixa', 'Moderada', 'Alta']
        df_final['nivel_desocupacao'] = np.select(condicoes, categorias, default='Moderada')
        
        # 4. Ordenar por data
        df_final = df_final.sort_values('data_referencia')
        
        # 5. Calcular média móvel (suaviza a linha)
        df_final['media_movel_4p'] = df_final['taxa_desocupacao'].rolling(window=4, min_periods=1).mean()
        
        # 6. Selecionar colunas finais
        colunas_finais = [
            'data_referencia', 'periodo', 'ano', 'trimestre',
            'taxa_desocupacao', 'variacao_periodo', 'vs_media_historica',
            'status', 'nivel_desocupacao', 'media_movel_4p', 'localidade'
        ]
        
        df_final = df_final[colunas_finais]
        
        # Salvar CSV final
        df_final.to_csv('pnad_powerbi_pronto.csv', index=False, encoding='utf-8-sig')
        
        print(" CSV FINAL CRIADO: pnad_powerbi_pronto.csv")
        print(f" Total de registros: {len(df_final)}")
        print(f" Período: {df_final['data_referencia'].min().year} a {df_final['data_referencia'].max().year}")
        print(f" Amostra dos dados:")
        print(df_final.head(3))
        
        # Criar arquivo de instruções
        criar_instrucoes_powerbi()
        
        return df_final
        
    except Exception as e:
        print(f" Erro: {e}")
        return None
    finally:
        conn.close()

def criar_instrucoes_powerbi():
    instrucoes = """
INSTRUÇÕES PARA POWER BI - ANÁLISE PNAD IBGE

1. IMPORTAR DADOS:
   - Abra Power BI Desktop
   - "Obter Dados" → "Texto/CSV"
   - Selecione: pnad_powerbi_pronto.csv
   - Clique em "Carregar"

2. VISUALIZAÇÕES RECOMENDADAS:

   PÁGINA 1: VISÃO GERAL
   - Gráfico de Linha: data_referencia X taxa_desocupacao
   - Cartão KPI: Última taxa_desocupacao
   - Cartão KPI: Média histórica
   - Gráfico de Barras: nivel_desocupacao (contagem)

   PÁGINA 2: ANÁLISE TEMPORAL  
   - Gráfico de Linha Dupla: taxa_desocupacao + media_movel_4p
   - Gráfico de Área: variacao_periodo
   - Tabela: Todos os períodos ordenados

   PÁGINA 3: INSIGHTS
   - Texto com análises baseadas nos dados
   - Recomendações para gestores

3. MEDIDAS DAX SUGERIDAS:
   Taxa Atual = MAX('pnad_powerbi_pronto'[taxa_desocupacao])
   Tendência = // lógica de alta/baixa
   Vs Média = [Taxa Atual] - AVERAGE([taxa_desocupacao])

FONTE: PNAD Contínua IBGE | Desenvolvido em Python
"""
    
    with open('instrucoes_powerbi.txt', 'w', encoding='utf-8') as f:
        f.write(instrucoes)
    
    print(" Instruções salvas: instrucoes_powerbi.txt")

if __name__ == "__main__":
    import numpy as np
    criar_dataset_powerbi()