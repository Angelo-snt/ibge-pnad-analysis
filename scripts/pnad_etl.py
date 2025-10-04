# analise_pnad.py
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import requests

def buscar_mais_dados_pnad():
    """Busca dados da PNAD para todos os períodos"""
    print("Buscando dados historicos da PNAD...")
    
    # URL para varios periodos
    url = "https://apisidra.ibge.gov.br/values/t/6381/n1/all/v/4099/p/all"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            print(f"Dados recebidos: {len(dados)} registros")
            
            df = pd.DataFrame(dados[1:], columns=dados[0])
            
            # Salvar no banco
            conn = sqlite3.connect('ibge_analise.db')
            df.to_sql('pnad_historico', conn, if_exists='replace', index=False)
            conn.close()
            
            print(f"Salvo: {df.shape[0]} registros historicos")
            return df
        else:
            print(f"Erro na API: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Erro: {e}")
        return None

def analisar_desemprego():
    """Analisa os dados de desemprego"""
    print("\nAnalisando dados de desemprego...")
    
    conn = sqlite3.connect('ibge_analise.db')
    
    try:
        # Ler dados
        df = pd.read_sql("SELECT * FROM pnad_historico", conn)
        
        if df.empty:
            print("Nenhum dado para analisar")
            return
        
        # Preparar dados para analise
        df['V'] = pd.to_numeric(df['V'], errors='coerce')  # Converte valor para numero
        df['periodo'] = df['D3N']  # Periodo
        
        # Analise basica
        print(f"Periodos analisados: {df['periodo'].nunique()}")
        print(f"Taxa media de desocupacao: {df['V'].mean():.2f}%")
        print(f"Maior taxa: {df['V'].max():.2f}%")
        print(f"Menor taxa: {df['V'].min():.2f}%")
        
        # Ultimos 5 periodos
        print("\nUltimos 5 periodos:")
        ultimos = df[['periodo', 'V']].tail(5)
        print(ultimos)
        
        return df
        
    except Exception as e:
        print(f"Erro na analise: {e}")
        return None
    finally:
        conn.close()

def criar_visualizacao(df):
    """Cria grafico simples"""
    if df is None or df.empty:
        print("Nao ha dados para visualizacao")
        return
    
    try:
        # Preparar dados para grafico
        df_plot = df.tail(8).copy()  # Ultimos 8 periodos
        df_plot = df_plot.sort_values('periodo')
        
        # Criar grafico
        plt.figure(figsize=(10, 6))
        plt.plot(df_plot['periodo'], df_plot['V'], marker='o', linewidth=2)
        plt.title('Evolucao da Taxa de Desocupacao - Brasil')
        plt.xlabel('Periodo')
        plt.ylabel('Taxa de Desocupacao (%)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Salvar grafico
        plt.savefig('evolucao_desemprego.png', dpi=300)
        print("Grafico salvo como 'evolucao_desemprego.png'")
        
        # Mostrar grafico
        plt.show()
        
    except Exception as e:
        print(f"Erro ao criar visualizacao: {e}")

def main():
    print("=" * 50)
    print("ANALISE PNAD - TAXA DE DESOCUPACAO")
    print("=" * 50)
    
    # 1. Buscar mais dados
    df = buscar_mais_dados_pnad()
    
    if df is not None:
        # 2. Analisar dados
        df_analise = analisar_desemprego()
        
        # 3. Criar visualizacao
        criar_visualizacao(df_analise)
    
    print("\n" + "=" * 50)
    print("ANALISE CONCLUIDA")
    print("=" * 50)

if __name__ == "__main__":
    main()