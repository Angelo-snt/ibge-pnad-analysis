# gerar_relatorio_pdf.py
from fpdf import FPDF
from datetime import datetime
import os

class RelatorioPNAD(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'RELATÓRIO TÉCNICO - ANÁLISE PNAD CONTÍNUA IBGE', 0, 1, 'C')
        self.line(10, 20, 200, 20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
    
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
    pdf.cell(0, 15, 'ANÁLISE PNAD CONTÍNUA IBGE', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Relatório Técnico - Processo de ETL e Análise', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Data de geração: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
    pdf.cell(0, 10, 'Vaga: Analista de Dados Sênior', 0, 1, 'C')
    pdf.ln(30)
    
    # 1. RESUMO EXECUTIVO
    pdf.chapter_title('1. RESUMO EXECUTIVO')
    pdf.body_text("""Este relatório documenta o processo completo de análise dos dados da PNAD Contínua do IBGE, desde a extração via API até a criação de dashboards interativos no Power BI.

Objetivo: Análise da taxa de desocupação brasileira através dos microdados oficiais
Período: 2012-2024 (162 trimestres)
Tecnologias: Python, Pandas, SQLite, Power BI
Entregáveis: Pipeline de ETL automatizado e dashboard com insights estratégicos""")
    
    # 2. METODOLOGIA
    pdf.chapter_title('2. METODOLOGIA')
    
    pdf.section_title('2.1. EXTRAÇÃO (E)')
    pdf.body_text("Dados obtidos através da API SIDRA do IBGE:")
    pdf.code_block("""# API endpoint
url = "https://apisidra.ibge.gov.br/values/t/6381/n1/all/v/4099/p/all"

# Parâmetros:
# t/6381 - PNAD Contínua Trimestral
# v/4099 - Taxa de desocupação
# p/all  - Todos os períodos disponíveis""")
    
    pdf.section_title('2.2. TRANSFORMAÇÃO (T)')
    pdf.body_text("Processos aplicados nos dados:")
    pdf.code_block("""# Script de transformação
- Limpeza de dados faltantes e inconsistentes
- Conversão de tipos (string para numérico)
- Criação de métricas derivadas (variação percentual)
- Normalização de nomes de colunas
- Cálculo de médias móveis (4 períodos)
- Classificação por categorias (Baixa/Moderada/Alta)""")
    
    pdf.section_title('2.3. CARREGAMENTO (L)')
    pdf.body_text("Destinos dos dados processados:")
    pdf.code_block("""# Pipeline de carregamento
1. Banco SQLite: ibge_analise.db (armazenamento local)
2. Arquivo CSV: pnad_powerbi_pronto.csv (Power BI)
3. Dataset otimizado para análise""")
    
    # 3. ARQUITETURA DA SOLUÇÃO
    pdf.chapter_title('3. ARQUITETURA DA SOLUÇÃO')
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
Insights e Relatórios""")
    
    pdf.section_title('3.1. Scripts Python Desenvolvidos')
    pdf.body_text("""pnad_etl.py - Pipeline principal de extração e transformação
verificar_dados.py - Validação e controle de qualidade
preparar_dados_powerbi.py - Otimização para visualização
powerbi_final.py - Geração do dataset final
gerar_relatorio_pdf.py - Este relatório""")
    
    pdf.section_title('3.2. Estrutura do Banco de Dados')
    pdf.code_block("""-- Tabelas no SQLite
pnad_historico (dados brutos da API)
powerbi_otimizado (dados tratados para análise)
dados_ibge_api (metadados e controles)""")
    
    # 4. ANÁLISE E INSIGHTS
    pdf.add_page()
    pdf.chapter_title('4. ANÁLISE E INSIGHTS')
    
    pdf.section_title('4.1. Principais Indicadores Calculados')
    pdf.body_text("""- Taxa de desocupação trimestral
- Variação percentual período a período
- Média histórica (2012-2024)
- Classificação por nível de desocupação
- Tendência (Alta/Baixa/Estável)
- Média móvel (suavização de tendências)""")
    
    pdf.section_title('4.2. Insights Identificados')
    pdf.body_text("""1. TENDÊNCIA DE LONGO PRAZO: Análise da evolução da taxa de desocupação ao longo de 12 anos
2. SAZONALIDADE: Identificação de padrões trimestrais recorrentes
3. IMPACTO DE EVENTOS: Análise do efeito de crises econômicas e pandêmicas
4. COMPARATIVO HISTÓRICO: Posicionamento atual em relação à média do período""")
    
    # 5. VISUALIZAÇÃO NO POWER BI
    pdf.chapter_title('5. VISUALIZAÇÃO NO POWER BI')
    
    pdf.section_title('5.1. Estrutura do Dashboard')
    pdf.body_text("""PÁGINA 1 - VISÃO GERAL
- Gráfico de linha evolutivo da taxa de desocupação
- KPIs principais (taxa atual, média histórica, variação)
- Indicadores de status e tendência

PÁGINA 2 - ANÁLISE DETALHADA
- Média móvel para suavização de tendências
- Análise por categorias de desocupação
- Tabela detalhada com todos os períodos

PÁGINA 3 - RECOMENDAÇÕES
- Insights acionáveis para gestores públicos
- Estratégias para empresas privadas""")
    
    pdf.section_title('5.2. Medidas DAX Implementadas')
    pdf.code_block("""// Taxa Atual (último período)
Taxa Atual = 
    CALCULATE(
        MAX([taxa_desocupação]),
        LASTDATE([data_referencia])
    )

// Tendência
Tendência = 
    VAR TaxaAtual = [Taxa Atual]
    VAR TaxaAnterior = [Taxa Período Anterior]
    RETURN
    IF(TaxaAtual > TaxaAnterior, "Alta",
       IF(TaxaAtual < TaxaAnterior, "Baixa", "Estável"))""")
    
    # 6. RESULTADOS E IMPACTOS
    pdf.add_page()
    pdf.chapter_title('6. RESULTADOS E IMPACTOS')
    
    pdf.section_title('6.1. Para Gestores Públicos')
    pdf.body_text("""- Identificação de períodos críticos para intervenção
- Base data-driven para políticas de geração de emprego
- Monitoramento da efetividade de programas sociais
- Análise de impacto de medidas econômicas""")
    
    pdf.section_title('6.2. Para Empresas Privadas')
    pdf.body_text("""- Análise de mercado para decisões de expansão
- Planejamento estratégico de contratações
- Estudo de cenários econômicos para investimentos
- Benchmarking do setor""")
    
    # 7. TECNOLOGIAS UTILIZADAS
    pdf.chapter_title('7. TECNOLOGIAS UTILIZADAS')
    
    pdf.body_text("""+-----------------+----------------------+-----------------------------+
|     Camada      |     Tecnologia       |         Finalidade          |
+-----------------+----------------------+-----------------------------+
|   Extração      |   Python Requests    |   Consumo da API IBGE       |
| Processamento   |   Pandas, NumPy      |   Transformação de dados    |
| Armazenamento   |   SQLite             |   Banco de dados local      |
| Visualização    |   Power BI           |   Dashboard interativo      |
| Documentação    |   FPDF (Python)      |   Relatório técnico         |
+-----------------+----------------------+-----------------------------+""")
    
    # 8. CONSIDERAÇÕES FINAIS
    pdf.chapter_title('8. CONSIDERAÇÕES FINAIS')
    
    pdf.section_title('8.1. Lições Aprendidas')
    pdf.body_text("""- Importância da validação de dados na fonte para qualidade
- Eficiência do pipeline Python para processos ETL complexos
- Valor da documentação completa do processo analítico
- Flexibilidade do SQLite para prototipagem e análise""")
    
    pdf.section_title('8.2. Próximos Passos Recomendados')
    pdf.body_text("""- Inclusão de dados regionais (análise por UF)
- Cruzamento com outras bases do IBGE (renda, educação)
- Automação da atualização trimestral dos dados
- Desenvolvimento de modelos preditivos simples
- Criação de alertas para tendências significativas""")
    
    # ANEXOS
    pdf.add_page()
    pdf.chapter_title('ANEXOS')
    
    pdf.section_title('Anexo A - Estrutura de Pastas do Projeto')
    pdf.code_block("""IBGE/
|-- pnad_etl.py (script principal)
|-- verificar_dados.py (validação)
|-- preparar_dados_powerbi.py (otimização)
|-- powerbi_final.py (dataset final)
|-- gerar_relatorio_pdf.py (este relatório)
|-- ibge_analise.db (banco SQLite)
|-- pnad_powerbi_pronto.csv (dados Power BI)
|-- instrucoes_powerbi.txt (guia de uso)""")
    
    pdf.section_title('Anexo B - Metadados dos Dados')
    pdf.body_text("""Fonte: PNAD Contínua - IBGE
Indicador principal: Taxa de desocupação (%)
Período coberto: 2012-2024
Frequência: Trimestral
Total de registros: 162 períodos
Última atualização: Dados mais recentes disponíveis""")
    
    # Assinatura
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'Documento gerado automaticamente via Python - Demonstrando habilidades técnicas em ETL e análise de dados', 0, 1, 'C')
    
    # Salvar PDF na pasta docs
    nome_arquivo = f'../docs/Relatorio_PNAD_IBGE_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf'
    pdf.output(nome_arquivo)
    
    print(f"PDF gerado com sucesso: {nome_arquivo}")
    print(f"Local: {os.path.abspath(nome_arquivo)}")
    
    return nome_arquivo

if __name__ == "__main__":
    arquivo_pdf = criar_relatorio_pdf()
    print(f"Relatório pronto! Arquivo: {arquivo_pdf}")