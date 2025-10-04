# gerar_relatorio_pdf.py
from fpdf import FPDF
from datetime import datetime
import os

class RelatorioPNAD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'RELATORIO TECNICO - ANALISE PNAD CONTINUA IBGE', 0, 1, 'C')
        self.line(10, 20, 200, 20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)
    
    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
    
    def body_text(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, text)
        self.ln(3)
    
    def code_block(self, code):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(0, 5, code, 0, 'L', True)
        self.ln(3)

def criar_relatorio_pdf():
    pdf = RelatorioPNAD()
    pdf.add_page()
    
    # Capa
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 40, '', 0, 1)
    pdf.cell(0, 15, 'ANALISE PNAD CONTINUA IBGE', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Relatorio Tecnico - Processo de ETL e Analise', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Data de geracao: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
    pdf.cell(0, 10, 'Vaga: Analista de Dados Senior', 0, 1, 'C')
    pdf.ln(30)
    
    # 1. RESUMO EXECUTIVO
    pdf.chapter_title('1. RESUMO EXECUTIVO')
    pdf.body_text("""Este relatorio documenta o processo completo de analise dos dados da PNAD Continua do IBGE, desde a extracao via API ate a criacao de dashboards interativos no Power BI.

Objetivo: Analise da taxa de desocupacao brasileira atraves dos microdados oficiais
Periodo: 2012-2024 (162 trimestres)
Tecnologias: Python, Pandas, SQLite, Power BI
Entregaveis: Pipeline de ETL automatizado e dashboard com insights estrategicos""")
    
    # 2. METODOLOGIA
    pdf.chapter_title('2. METODOLOGIA')
    
    pdf.section_title('2.1. EXTRACAO (E)')
    pdf.body_text("Dados obtidos atraves da API SIDRA do IBGE:")
    pdf.code_block("""# API endpoint
url = "https://apisidra.ibge.gov.br/values/t/6381/n1/all/v/4099/p/all"

# Parametros:
# t/6381 - PNAD Continua Trimestral
# v/4099 - Taxa de desocupacao
# p/all  - Todos os periodos disponiveis""")
    
    pdf.section_title('2.2. TRANSFORMACAO (T)')
    pdf.body_text("Processos aplicados nos dados:")
    pdf.code_block("""# Script de transformacao
- Limpeza de dados faltantes e inconsistentes
- Conversao de tipos (string para numerico)
- Criacao de metricas derivadas (variacao percentual)
- Normalizacao de nomes de colunas
- Calculo de medias moveis (4 periodos)
- Classificacao por categorias (Baixa/Moderada/Alta)""")
    
    pdf.section_title('2.3. CARREGAMENTO (L)')
    pdf.body_text("Destinos dos dados processados:")
    pdf.code_block("""# Pipeline de carregamento
1. Banco SQLite: ibge_analise.db (armazenamento local)
2. Arquivo CSV: pnad_powerbi_pronto.csv (Power BI)
3. Dataset otimizado para analise""")
    
    # 3. ARQUITETURA DA SOLUCAO
    pdf.chapter_title('3. ARQUITETURA DA SOLUCAO')
    pdf.body_text("Fluxo completo de dados implementado:")
    pdf.code_block("""ARQUITETURA DO PROJETO:

API IBGE (REST) 
    |
Python Scripts (ETL)
    |
SQLite Database 
    |
CSV Otimizado
    |
Power BI Dashboard
    |
Insights e Relatorios""")
    
    pdf.section_title('3.1. Scripts Python Desenvolvidos')
    pdf.body_text("""pnad_etl.py - Pipeline principal de extracao e transformacao
verificar_dados.py - Validacao e controle de qualidade
preparar_dados_powerbi.py - Otimizacao para visualizacao
powerbi_final.py - Geracao do dataset final
gerar_relatorio_pdf.py - Este relatorio""")
    
    pdf.section_title('3.2. Estrutura do Banco de Dados')
    pdf.code_block("""-- Tabelas no SQLite
pnad_historico (dados brutos da API)
powerbi_otimizado (dados tratados para analise)
dados_ibge_api (metadados e controles)""")
    
    # 4. ANALISE E INSIGHTS
    pdf.add_page()
    pdf.chapter_title('4. ANALISE E INSIGHTS')
    
    pdf.section_title('4.1. Principais Indicadores Calculados')
    pdf.body_text("""- Taxa de desocupacao trimestral
- Variacao percentual periodo a periodo
- Media historica (2012-2024)
- Classificacao por nivel de desocupacao
- Tendencia (Alta/Baixa/Estavel)
- Media movel (suavizacao de tendencias)""")
    
    pdf.section_title('4.2. Insights Identificados')
    pdf.body_text("""1. TENDENCIA DE LONGO PRAZO: Analise da evolucao da taxa de desocupacao ao longo de 12 anos
2. SAZONALIDADE: Identificacao de padroes trimestrais recorrentes
3. IMPACTO DE EVENTOS: Analise do efeito de crises economicas e pandemicas
4. COMPARATIVO HISTORICO: Posicionamento atual em relacao a media do periodo""")
    
    # 5. VISUALIZACAO NO POWER BI
    pdf.chapter_title('5. VISUALIZACAO NO POWER BI')
    
    pdf.section_title('5.1. Estrutura do Dashboard')
    pdf.body_text("""PAGINA 1 - VISAO GERAL
- Grafico de linha evolutivo da taxa de desocupacao
- KPIs principais (taxa atual, media historica, variacao)
- Indicadores de status e tendencia

PAGINA 2 - ANALISE DETALHADA
- Media movel para suavizacao de tendencias
- Analise por categorias de desocupacao
- Tabela detalhada com todos os periodos

PAGINA 3 - RECOMENDACOES
- Insights acionaveis para gestores publicos
- Estrategias para empresas privadas""")
    
    pdf.section_title('5.2. Medidas DAX Implementadas')
    pdf.code_block("""// Taxa Atual (ultimo periodo)
Taxa Atual = 
    CALCULATE(
        MAX([taxa_desocupacao]),
        LASTDATE([data_referencia])
    )

// Tendencia
Tendencia = 
    VAR TaxaAtual = [Taxa Atual]
    VAR TaxaAnterior = [Taxa Periodo Anterior]
    RETURN
    IF(TaxaAtual > TaxaAnterior, "Alta",
       IF(TaxaAtual < TaxaAnterior, "Baixa", "Estavel"))""")
    
    # 6. RESULTADOS E IMPACTOS
    pdf.add_page()
    pdf.chapter_title('6. RESULTADOS E IMPACTOS')
    
    pdf.section_title('6.1. Para Gestores Publicos')
    pdf.body_text("""- Identificacao de periodos criticos para intervencao
- Base data-driven para politicas de geracao de emprego
- Monitoramento da efetividade de programas sociais
- Analise de impacto de medidas economicas""")
    
    pdf.section_title('6.2. Para Empresas Privadas')
    pdf.body_text("""- Analise de mercado para decisoes de expansao
- Planejamento estrategico de contratacoes
- Estudo de cenarios economicos para investimentos
- Benchmarking do setor""")
    
    # 7. TECNOLOGIAS UTILIZADAS
    pdf.chapter_title('7. TECNOLOGIAS UTILIZADAS')
    
    pdf.body_text("""+-----------------+----------------------+-----------------------------+
|     Camada      |     Tecnologia       |         Finalidade          |
+-----------------+----------------------+-----------------------------+
|   Extracao      |   Python Requests    |   Consumo da API IBGE       |
| Processamento   |   Pandas, NumPy      |   Transformacao de dados    |
| Armazenamento   |   SQLite             |   Banco de dados local      |
| Visualizacao    |   Power BI           |   Dashboard interativo      |
| Documentacao    |   FPDF (Python)      |   Relatorio tecnico         |
+-----------------+----------------------+-----------------------------+""")
    
    # 8. CONSIDERACOES FINAIS
    pdf.chapter_title('8. CONSIDERACOES FINAIS')
    
    pdf.section_title('8.1. Licoes Aprendidas')
    pdf.body_text("""- Importancia da validacao de dados na fonte para qualidade
- Eficiencia do pipeline Python para processos ETL complexos
- Valor da documentacao completa do processo analitico
- Flexibilidade do SQLite para prototipagem e analise""")
    
    pdf.section_title('8.2. Proximos Passos Recomendados')
    pdf.body_text("""- Inclusao de dados regionais (analise por UF)
- Cruzamento com outras bases do IBGE (renda, educacao)
- Automacao da atualizacao trimestral dos dados
- Desenvolvimento de modelos preditivos simples
- Criacao de alertas para tendencias significativas""")
    
    # ANEXOS
    pdf.add_page()
    pdf.chapter_title('ANEXOS')
    
    pdf.section_title('Anexo A - Estrutura de Pastas do Projeto')
    pdf.code_block("""IBGE/
|-- pnad_etl.py (script principal)
|-- verificar_dados.py (validacao)
|-- preparar_dados_powerbi.py (otimizacao)
|-- powerbi_final.py (dataset final)
|-- gerar_relatorio_pdf.py (este relatorio)
|-- ibge_analise.db (banco SQLite)
|-- pnad_powerbi_pronto.csv (dados Power BI)
|-- instrucoes_powerbi.txt (guia de uso)""")
    
    pdf.section_title('Anexo B - Metadados dos Dados')
    pdf.body_text("""Fonte: PNAD Continua - IBGE
Indicador principal: Taxa de desocupacao (%)
Periodo coberto: 2012-2024
Frequencia: Trimestral
Total de registros: 162 periodos
Ultima atualizacao: Dados mais recentes disponiveis""")
    
    # Assinatura
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'Documento gerado automaticamente via Python - Demonstrando habilidades tecnicas em ETL e analise de dados', 0, 1, 'C')
    
    # Salvar PDF
    nome_arquivo = f'Relatorio_PNAD_IBGE_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf'
    pdf.output(nome_arquivo)
    
    print(f"PDF gerado com sucesso: {nome_arquivo}")
    print(f"Local: {os.path.abspath(nome_arquivo)}")
    
    return nome_arquivo

if __name__ == "__main__":
    arquivo_pdf = criar_relatorio_pdf()
    print(f"Relatorio pronto! Arquivo: {arquivo_pdf}")