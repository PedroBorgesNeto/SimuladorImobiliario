import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import locale
from datetime import datetime

# Configurar localização para formatação de moeda em português brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass  # Fallback para configuração padrão

# Classe SimuladorImovel
class SimuladorImovel:
    """Classe principal do simulador de opções imobiliárias."""
    
    def __init__(self):
        """Inicializa o simulador com valores padrão."""
        # Parâmetros padrão
        self.valor_imovel = 500000.0
        self.percentual_aluguel = 0.004  # 0.4% do valor do imóvel por mês
        self.taxa_juros_investimento = 0.08  # 8% ao ano
        self.taxa_juros_financiamento = 0.10  # 10% ao ano
        self.taxa_valorizacao_imovel = 0.05  # 5% ao ano
        self.percentual_financiamento = 0.50  # 50% financiado
        self.prazo_financiamento = 20  # 20 anos
        self.prazo_simulacao = 30  # 30 anos para simulação completa
        
        # Resultados
        self.resultados = {}
        
    def definir_parametros(self, valor_imovel=None, percentual_aluguel=None, 
                          taxa_juros_investimento=None, taxa_juros_financiamento=None,
                          taxa_valorizacao_imovel=None, percentual_financiamento=None,
                          prazo_financiamento=None, prazo_simulacao=None):
        """Define os parâmetros da simulação."""
        if valor_imovel is not None:
            self.valor_imovel = valor_imovel
        if percentual_aluguel is not None:
            self.percentual_aluguel = percentual_aluguel
        if taxa_juros_investimento is not None:
            self.taxa_juros_investimento = taxa_juros_investimento
        if taxa_juros_financiamento is not None:
            self.taxa_juros_financiamento = taxa_juros_financiamento
        if taxa_valorizacao_imovel is not None:
            self.taxa_valorizacao_imovel = taxa_valorizacao_imovel
        if percentual_financiamento is not None:
            self.percentual_financiamento = percentual_financiamento
        if prazo_financiamento is not None:
            self.prazo_financiamento = prazo_financiamento
        if prazo_simulacao is not None:
            self.prazo_simulacao = prazo_simulacao
    
    def calcular_aluguel(self):
        """Calcula a evolução patrimonial na opção de aluguel."""
        # Inicialização de variáveis
        valor_aluguel_mensal = self.valor_imovel * self.percentual_aluguel
        taxa_juros_mensal = (1 + self.taxa_juros_investimento) ** (1/12) - 1
        taxa_valorizacao_mensal = (1 + self.taxa_valorizacao_imovel) ** (1/12) - 1
        
        # Criação do DataFrame para armazenar os resultados
        meses = self.prazo_simulacao * 12
        df = pd.DataFrame(index=range(meses + 1))
        
        # Valores iniciais
        df.loc[0, 'Mês'] = 0
        df.loc[0, 'Patrimônio'] = self.valor_imovel  # Começa com o valor equivalente ao imóvel
        df.loc[0, 'Investimento'] = self.valor_imovel
        df.loc[0, 'Aluguel Mensal'] = valor_aluguel_mensal
        df.loc[0, 'Aluguel Acumulado'] = 0
        df.loc[0, 'Valor Imóvel'] = self.valor_imovel
        
        # Cálculo mês a mês
        for mes in range(1, meses + 1):
            # Atualização do valor do imóvel
            valor_imovel_atual = self.valor_imovel * (1 + taxa_valorizacao_mensal) ** mes
            
            # Atualização do valor do aluguel (acompanha a valorização do imóvel)
            valor_aluguel_atual = valor_imovel_atual * self.percentual_aluguel
            
            # Investimento cresce com juros e é reduzido pelo aluguel
            investimento_anterior = df.loc[mes-1, 'Investimento']
            investimento_atual = investimento_anterior * (1 + taxa_juros_mensal) - valor_aluguel_atual
            
            # Aluguel acumulado
            aluguel_acumulado = df.loc[mes-1, 'Aluguel Acumulado'] + valor_aluguel_atual
            
            # Registro dos valores
            df.loc[mes, 'Mês'] = mes
            df.loc[mes, 'Patrimônio'] = investimento_atual
            df.loc[mes, 'Investimento'] = investimento_atual
            df.loc[mes, 'Aluguel Mensal'] = valor_aluguel_atual
            df.loc[mes, 'Aluguel Acumulado'] = aluguel_acumulado
            df.loc[mes, 'Valor Imóvel'] = valor_imovel_atual
        
        self.resultados['aluguel'] = df
        return df
    
    def calcular_compra_vista(self):
        """Calcula a evolução patrimonial na opção de compra à vista."""
        # Inicialização de variáveis
        taxa_valorizacao_mensal = (1 + self.taxa_valorizacao_imovel) ** (1/12) - 1
        
        # Criação do DataFrame para armazenar os resultados
        meses = self.prazo_simulacao * 12
        df = pd.DataFrame(index=range(meses + 1))
        
        # Valores iniciais
        df.loc[0, 'Mês'] = 0
        df.loc[0, 'Patrimônio'] = self.valor_imovel
        df.loc[0, 'Valor Imóvel'] = self.valor_imovel
        df.loc[0, 'Investimento'] = 0
        
        # Cálculo mês a mês
        for mes in range(1, meses + 1):
            # Atualização do valor do imóvel
            valor_imovel_atual = self.valor_imovel * (1 + taxa_valorizacao_mensal) ** mes
            
            # Registro dos valores
            df.loc[mes, 'Mês'] = mes
            df.loc[mes, 'Patrimônio'] = valor_imovel_atual
            df.loc[mes, 'Valor Imóvel'] = valor_imovel_atual
            df.loc[mes, 'Investimento'] = 0
        
        self.resultados['compra_vista'] = df
        return df
    
    def calcular_compra_financiada(self):
        """Calcula a evolução patrimonial na opção de compra financiada."""
        # Inicialização de variáveis
        valor_financiado = self.valor_imovel * self.percentual_financiamento
        valor_entrada = self.valor_imovel - valor_financiado
        
        taxa_juros_mensal = (1 + self.taxa_juros_financiamento) ** (1/12) - 1
        taxa_juros_investimento_mensal = (1 + self.taxa_juros_investimento) ** (1/12) - 1
        taxa_valorizacao_mensal = (1 + self.taxa_valorizacao_imovel) ** (1/12) - 1
        
        # Cálculo da prestação do financiamento (Sistema de Amortização Constante - SAC)
        amortizacao_mensal = valor_financiado / (self.prazo_financiamento * 12)
        
        # Criação do DataFrame para armazenar os resultados
        meses = self.prazo_simulacao * 12
        df = pd.DataFrame(index=range(meses + 1))
        
        # Valores iniciais
        df.loc[0, 'Mês'] = 0
        df.loc[0, 'Patrimônio'] = self.valor_imovel
        df.loc[0, 'Valor Imóvel'] = self.valor_imovel
        df.loc[0, 'Saldo Devedor'] = valor_financiado
        df.loc[0, 'Investimento'] = valor_entrada
        df.loc[0, 'Prestação'] = 0
        df.loc[0, 'Juros Pagos'] = 0
        df.loc[0, 'Juros Acumulados'] = 0
        
        # Cálculo mês a mês
        for mes in range(1, meses + 1):
            # Atualização do valor do imóvel
            valor_imovel_atual = self.valor_imovel * (1 + taxa_valorizacao_mensal) ** mes
            
            # Cálculo do saldo devedor e prestação (apenas durante o período de financiamento)
            if mes <= self.prazo_financiamento * 12:
                saldo_devedor_anterior = df.loc[mes-1, 'Saldo Devedor']
                juros_mensais = saldo_devedor_anterior * taxa_juros_mensal
                prestacao = amortizacao_mensal + juros_mensais
                saldo_devedor_atual = saldo_devedor_anterior - amortizacao_mensal
                juros_acumulados = df.loc[mes-1, 'Juros Acumulados'] + juros_mensais
            else:
                saldo_devedor_atual = 0
                prestacao = 0
                juros_mensais = 0
                juros_acumulados = df.loc[mes-1, 'Juros Acumulados']
            
            # Atualização do investimento
            investimento_anterior = df.loc[mes-1, 'Investimento']
            investimento_atual = investimento_anterior * (1 + taxa_juros_investimento_mensal) - prestacao
            
            # Patrimônio total = valor do imóvel - saldo devedor + investimentos
            patrimonio = valor_imovel_atual - saldo_devedor_atual + max(0, investimento_atual)
            
            # Registro dos valores
            df.loc[mes, 'Mês'] = mes
            df.loc[mes, 'Patrimônio'] = patrimonio
            df.loc[mes, 'Valor Imóvel'] = valor_imovel_atual
            df.loc[mes, 'Saldo Devedor'] = saldo_devedor_atual
            df.loc[mes, 'Investimento'] = max(0, investimento_atual)
            df.loc[mes, 'Prestação'] = prestacao
            df.loc[mes, 'Juros Pagos'] = juros_mensais
            df.loc[mes, 'Juros Acumulados'] = juros_acumulados
        
        self.resultados['compra_financiada'] = df
        return df
    
    def executar_simulacao(self):
        """Executa a simulação completa para as três opções."""
        self.calcular_aluguel()
        self.calcular_compra_vista()
        self.calcular_compra_financiada()
        return self.resultados
    
    def formatar_moeda(self, valor):
        """Formata um valor como moeda brasileira."""
        try:
            return locale.currency(valor, grouping=True)
        except:
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def analisar_riscos_beneficios(self):
        """Analisa os riscos e benefícios de cada opção."""
        analise = {
            'aluguel': {
                'beneficios': [
                    'Maior liquidez do patrimônio',
                    'Flexibilidade para mudança de localização',
                    'Sem custos de manutenção e IPTU',
                    'Sem risco de desvalorização do imóvel',
                    'Sem necessidade de grande capital inicial'
                ],
                'riscos': [
                    'Aumento do valor do aluguel acima da inflação',
                    'Rendimento dos investimentos pode cair',
                    'Insegurança quanto à renovação do contrato',
                    'Limitações para personalização do imóvel',
                    'Não formação de patrimônio imobiliário'
                ]
            },
            'compra_vista': {
                'beneficios': [
                    'Ausência de juros e encargos financeiros',
                    'Segurança da propriedade imediata',
                    'Potencial de valorização do imóvel',
                    'Liberdade para personalização do imóvel',
                    'Redução de despesas mensais fixas'
                ],
                'riscos': [
                    'Imobilização de capital significativo',
                    'Baixa liquidez do patrimônio',
                    'Risco de desvalorização do imóvel',
                    'Custos de manutenção, IPTU e condomínio',
                    'Custo de oportunidade do capital não investido'
                ]
            },
            'compra_financiada': {
                'beneficios': [
                    'Preservação de parte do capital para investimentos',
                    'Seguro patrimonial e de vida incluído no financiamento',
                    'Possibilidade de renegociação da dívida com queda nos juros',
                    'Opção de quitação antecipada',
                    'Juros pagos elevam o valor de aquisição, reduzindo IR sobre ganho de capital',
                    'Valorização do imóvel com queda nos juros'
                ],
                'riscos': [
                    'Custo total elevado devido aos juros do financiamento',
                    'Comprometimento da renda por longo período',
                    'Risco de inadimplência em caso de perda de renda',
                    'Possível desvalorização do imóvel',
                    'Rendimento dos investimentos pode ficar abaixo do custo do financiamento'
                ]
            }
        }
        
        return analise

# Função para formatar moeda
def formatar_moeda(valor):
    try:
        return locale.currency(valor, grouping=True)
    except:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Função para formatar percentual
def formatar_percentual(valor):
    return f"{valor*100:.2f}%"

# Configuração da página
st.set_page_config(
    page_title="Simulador de Opções Imobiliárias",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏠 Simulador de Opções Imobiliárias")

st.markdown("""
Este simulador compara três alternativas para aquisição de imóvel:
1. **Aluguel**: Alugar o imóvel e investir o valor equivalente à compra
2. **Compra à Vista**: Adquirir o imóvel com pagamento integral
3. **Compra Financiada**: Adquirir o imóvel com entrada parcial e financiamento
""")

# Criar abas
tab1, tab2, tab3 = st.tabs(["Simulador", "Resultados Detalhados", "Riscos e Benefícios"])

with tab1:
    # Sidebar para parâmetros de entrada
    st.sidebar.header("Parâmetros da Simulação")
    
    # Criar instância do simulador
    simulador = SimuladorImovel()
    
    # Parâmetros do imóvel
    st.sidebar.subheader("Imóvel")
    valor_imovel = st.sidebar.number_input(
        "Valor do Imóvel (R$)",
        min_value=100000.0,
        max_value=10000000.0,
        value=simulador.valor_imovel,
        step=50000.0,
        format="%.2f"
    )
    
    percentual_aluguel = st.sidebar.slider(
        "Aluguel Mensal (% do valor do imóvel)",
        min_value=0.1,
        max_value=1.0,
        value=simulador.percentual_aluguel * 100,
        step=0.05,
        format="%.2f%%"
    ) / 100
    
    taxa_valorizacao_imovel = st.sidebar.slider(
        "Valorização Anual do Imóvel (%)",
        min_value=0.0,
        max_value=15.0,
        value=simulador.taxa_valorizacao_imovel * 100,
        step=0.5,
        format="%.2f%%"
    ) / 100
    
    # Parâmetros financeiros
    st.sidebar.subheader("Investimentos")
    taxa_juros_investimento = st.sidebar.slider(
        "Rendimento Anual dos Investimentos (% livre de IR)",
        min_value=0.0,
        max_value=15.0,
        value=simulador.taxa_juros_investimento * 100,
        step=0.5,
        format="%.2f%%"
    ) / 100
    
    # Parâmetros do financiamento
    st.sidebar.subheader("Financiamento")
    percentual_financiamento = st.sidebar.slider(
        "Percentual Financiado (%)",
        min_value=10.0,
        max_value=90.0,
        value=simulador.percentual_financiamento * 100,
        step=5.0,
        format="%.1f%%"
    ) / 100
    
    taxa_juros_financiamento = st.sidebar.slider(
        "Taxa de Juros Anual do Financiamento (%)",
        min_value=5.0,
        max_value=20.0,
        value=simulador.taxa_juros_financiamento * 100,
        step=0.5,
        format="%.2f%%"
    ) / 100
    
    prazo_financiamento = st.sidebar.slider(
        "Prazo do Financiamento (anos)",
        min_value=5,
        max_value=35,
        value=simulador.prazo_financiamento,
        step=1
    )
    
    # Parâmetros da simulação
    st.sidebar.subheader("Simulação")
    prazo_simulacao = st.sidebar.slider(
        "Prazo da Simulação (anos)",
        min_value=5,
        max_value=50,
        value=simulador.prazo_simulacao,
        step=5
    )
    
    # Atualizar parâmetros do simulador
    simulador.definir_parametros(
        valor_imovel=valor_imovel,
        percentual_aluguel=percentual_aluguel,
        taxa_juros_investimento=taxa_juros_investimento,
        taxa_juros_financiamento=taxa_juros_financiamento,
        taxa_valorizacao_imovel=taxa_valorizacao_imovel,
        percentual_financiamento=percentual_financiamento,
        prazo_financiamento=prazo_financiamento,
        prazo_simulacao=prazo_simulacao
    )
    
    # Executar simulação
    resultados = simulador.executar_simulacao()
    
    # Exibir resumo dos parâmetros
    st.subheader("Resumo dos Parâmetros")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Valor do Imóvel", formatar_moeda(valor_imovel))
        st.metric("Aluguel Mensal", formatar_moeda(valor_imovel * percentual_aluguel))
    
    with col2:
        st.metric("Rendimento Investimentos", formatar_percentual(taxa_juros_investimento))
        st.metric("Valorização do Imóvel", formatar_percentual(taxa_valorizacao_imovel))
    
    with col3:
        st.metric("Valor Financiado", formatar_moeda(valor_imovel * percentual_financiamento))
        st.metric("Juros do Financiamento", formatar_percentual(taxa_juros_financiamento))
    
    # Exibir gráfico de evolução patrimonial
    st.subheader("Evolução Patrimonial")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Formatador para exibir valores em reais
    def formatar_eixo_y(valor, pos):
        if valor >= 1e6:
            return f'R$ {valor/1e6:.1f}M'
        else:
            return f'R$ {valor/1e3:.0f}K'
    
    formatter = plt.FuncFormatter(formatar_eixo_y)
    
    # Plotar os dados
    ax.plot(resultados['aluguel']['Mês'] / 12, 
             resultados['aluguel']['Patrimônio'], 
             label='Aluguel', linewidth=2)
    
    ax.plot(resultados['compra_vista']['Mês'] / 12, 
             resultados['compra_vista']['Patrimônio'], 
             label='Compra à Vista', linewidth=2)
    
    ax.plot(resultados['compra_financiada']['Mês'] / 12, 
             resultados['compra_financiada']['Patrimônio'], 
             label='Compra Financiada', linewidth=2)
    
    # Configurações do gráfico
    ax.set_xlabel('Anos')
    ax.set_ylabel('Patrimônio Total')
    ax.set_title('Comparação da Evolução Patrimonial')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    ax.yaxis.set_major_formatter(formatter)
    
    st.pyplot(fig)
    
    # Exibir tabela comparativa
    st.subheader("Comparação dos Resultados")
    
    # Extrair resultados finais
    resultado_aluguel = resultados['aluguel'].iloc[-1]
    resultado_compra_vista = resultados['compra_vista'].iloc[-1]
    resultado_compra_financiada = resultados['compra_financiada'].iloc[-1]
    
    # Criar DataFrame comparativo
    comparacao = pd.DataFrame({
        'Métrica': [
            'Patrimônio Final',
            'Valor Final do Imóvel',
            'Investimento Final',
            'Aluguel Total Pago',
            'Juros Totais Pagos',
            'Retorno sobre Investimento (%)'
        ],
        'Aluguel': [
            formatar_moeda(resultado_aluguel['Patrimônio']),
            formatar_moeda(resultado_aluguel['Valor Imóvel']),
            formatar_moeda(resultado_aluguel['Investimento']),
            formatar_moeda(resultado_aluguel['Aluguel Acumulado']),
            'N/A',
            f"{(resultado_aluguel['Patrimônio'] / valor_imovel - 1) * 100:.2f}%"
        ],
        'Compra à Vista': [
            formatar_moeda(resultado_compra_vista['Patrimônio']),
            formatar_moeda(resultado_compra_vista['Valor Imóvel']),
            'N/A',
            'N/A',
            'N/A',
            f"{(resultado_compra_vista['Patrimônio'] / valor_imovel - 1) * 100:.2f}%"
        ],
        'Compra Financiada': [
            formatar_moeda(resultado_compra_financiada['Patrimônio']),
            formatar_moeda(resultado_compra_financiada['Valor Imóvel']),
            formatar_moeda(resultado_compra_financiada['Investimento']),
            'N/A',
            formatar_moeda(resultado_compra_financiada['Juros Acumulados']),
            f"{(resultado_compra_financiada['Patrimônio'] / valor_imovel - 1) * 100:.2f}%"
        ]
    })
    
    st.table(comparacao)
    
    # Conclusão
    st.subheader("Conclusão")
    
    # Determinar a melhor opção com base no patrimônio final
    patrimonio_aluguel = resultado_aluguel['Patrimônio']
    patrimonio_compra_vista = resultado_compra_vista['Patrimônio']
    patrimonio_compra_financiada = resultado_compra_financiada['Patrimônio']
    
    patrimonios = {
        "Aluguel": patrimonio_aluguel,
        "Compra à Vista": patrimonio_compra_vista,
        "Compra Financiada": patrimonio_compra_financiada
    }
    
    melhor_opcao = max(patrimonios, key=patrimonios.get)
    
    st.markdown(f"""
    Com base nos parâmetros informados, a opção com maior patrimônio final após {prazo_simulacao} anos é:
    
    ### {melhor_opcao}
    
    Com um patrimônio final de {formatar_moeda(patrimonios[melhor_opcao])}.
    
    > **Nota:** Esta conclusão considera apenas o aspecto financeiro. Fatores pessoais como segurança, flexibilidade e preferências individuais também devem ser considerados na decisão final.
    """)

with tab2:
    st.header("Resultados Detalhados")
    
    opcao = st.selectbox(
        "Selecione a opção para ver detalhes:",
        ["Aluguel", "Compra à Vista", "Compra Financiada"]
    )
    
    if opcao == "Aluguel":
        df = resultados['aluguel']
        st.subheader("Detalhes da Opção de Aluguel")
        
        # Converter meses para anos para melhor visualização
        df_anual = df[df['Mês'] % 12 == 0].copy()
        df_anual['Ano'] = df_anual['Mês'] / 12
        
        # Selecionar colunas relevantes
        colunas = ['Ano', 'Patrimônio', 'Investimento', 'Aluguel Mensal', 'Aluguel Acumulado', 'Valor Imóvel']
        
        # Formatar valores monetários
        df_formatado = df_anual[colunas].copy()
        for col in colunas[1:]:
            df_formatado[col] = df_formatado[col].apply(formatar_moeda)
        
        st.dataframe(df_formatado)
        
    elif opcao == "Compra à Vista":
        df = resultados['compra_vista']
        st.subheader("Detalhes da Opção de Compra à Vista")
        
        # Converter meses para anos para melhor visualização
        df_anual = df[df['Mês'] % 12 == 0].copy()
        df_anual['Ano'] = df_anual['Mês'] / 12
        
        # Selecionar colunas relevantes
        colunas = ['Ano', 'Patrimônio', 'Valor Imóvel']
        
        # Formatar valores monetários
        df_formatado = df_anual[colunas].copy()
        for col in colunas[1:]:
            df_formatado[col] = df_formatado[col].apply(formatar_moeda)
        
        st.dataframe(df_formatado)
        
    else:  # Compra Financiada
        df = resultados['compra_financiada']
        st.subheader("Detalhes da Opção de Compra Financiada")
        
        # Converter meses para anos para melhor visualização
        df_anual = df[df['Mês'] % 12 == 0].copy()
        df_anual['Ano'] = df_anual['Mês'] / 12
        
        # Selecionar colunas relevantes
        colunas = ['Ano', 'Patrimônio', 'Valor Imóvel', 'Saldo Devedor', 'Investimento', 'Prestação', 'Juros Acumulados']
        
        # Formatar valores monetários
        df_formatado = df_anual[colunas].copy()
        for col in colunas[1:]:
            df_formatado[col] = df_formatado[col].apply(formatar_moeda)
        
        st.dataframe(df_formatado)
    
    # Gráficos adicionais
    st.subheader("Gráficos Adicionais")
    
    grafico_opcao = st.selectbox(
        "Selecione o gráfico:",
        ["Comparação de Patrimônio", "Evolução do Valor do Imóvel", "Comparação de Investimentos"]
    )
    
    if grafico_opcao == "Comparação de Patrimônio":
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(resultados['aluguel']['Mês'] / 12, 
                 resultados['aluguel']['Patrimônio'], 
                 label='Aluguel', linewidth=2)
        
        ax.plot(resultados['compra_vista']['Mês'] / 12, 
                 resultados['compra_vista']['Patrimônio'], 
                 label='Compra à Vista', linewidth=2)
        
        ax.plot(resultados['compra_financiada']['Mês'] / 12, 
                 resultados['compra_financiada']['Patrimônio'], 
                 label='Compra Financiada', linewidth=2)
        
        ax.set_xlabel('Anos')
        ax.set_ylabel('Patrimônio Total')
        ax.set_title('Comparação da Evolução Patrimonial')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(formatar_eixo_y))
        
        st.pyplot(fig)
        
    elif grafico_opcao == "Evolução do Valor do Imóvel":
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(resultados['aluguel']['Mês'] / 12, 
                 resultados['aluguel']['Valor Imóvel'], 
                 label='Valor do Imóvel', linewidth=2)
        
        ax.set_xlabel('Anos')
        ax.set_ylabel('Valor do Imóvel')
        ax.set_title('Evolução do Valor do Imóvel')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(formatar_eixo_y))
        
        st.pyplot(fig)
        
    else:  # Comparação de Investimentos
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(resultados['aluguel']['Mês'] / 12, 
                 resultados['aluguel']['Investimento'], 
                 label='Investimento (Aluguel)', linewidth=2)
        
        ax.plot(resultados['compra_financiada']['Mês'] / 12, 
                 resultados['compra_financiada']['Investimento'], 
                 label='Investimento (Financiamento)', linewidth=2)
        
        ax.set_xlabel('Anos')
        ax.set_ylabel('Valor do Investimento')
        ax.set_title('Comparação dos Investimentos')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(formatar_eixo_y))
        
        st.pyplot(fig)

with tab3:
    st.header("Análise de Riscos e Benefícios")
    
    # Obter análise de riscos e benefícios
    analise = simulador.analisar_riscos_beneficios()
    
    # Exibir análise em formato de tabela
    opcao_tab3 = st.radio(
        "Selecione a opção para ver riscos e benefícios:",
        ["Aluguel", "Compra à Vista", "Compra Financiada"]
    )
    
    if opcao_tab3 == "Aluguel":
        chave = 'aluguel'
        titulo = "ALUGUEL"
    elif opcao_tab3 == "Compra à Vista":
        chave = 'compra_vista'
        titulo = "COMPRA À VISTA"
    else:
        chave = 'compra_financiada'
        titulo = "COMPRA FINANCIADA"
    
    st.subheader(f"Riscos e Benefícios: {titulo}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Benefícios")
        for i, beneficio in enumerate(analise[chave]['beneficios'], 1):
            st.markdown(f"**{i}.** {beneficio}")
    
    with col2:
        st.markdown("### Riscos")
        for i, risco in enumerate(analise[chave]['riscos'], 1):
            st.markdown(f"**{i}.** {risco}")
    
    # Exibir comparação geral
    st.subheader("Comparação Geral de Riscos e Benefícios")
    
    # Criar tabela comparativa
    beneficios_df = pd.DataFrame({
        'Aluguel': analise['aluguel']['beneficios'],
        'Compra à Vista': analise['compra_vista']['beneficios'],
        'Compra Financiada': analise['compra_financiada']['beneficios']
    })
    
    riscos_df = pd.DataFrame({
        'Aluguel': analise['aluguel']['riscos'],
        'Compra à Vista': analise['compra_vista']['riscos'],
        'Compra Financiada': analise['compra_financiada']['riscos']
    })
    
    st.markdown("### Benefícios Comparados")
    st.dataframe(beneficios_df)
    
    st.markdown("### Riscos Comparados")
    st.dataframe(riscos_df)
    
    # Considerações adicionais
    st.subheader("Considerações Adicionais")
    
    st.markdown("""
    ### Fatores que podem influenciar a decisão:
    
    1. **Estabilidade financeira**: A compra financiada requer estabilidade de renda a longo prazo.
    
    2. **Planos futuros**: Se há possibilidade de mudança de cidade ou país nos próximos anos, o aluguel oferece mais flexibilidade.
    
    3. **Mercado imobiliário local**: Em algumas regiões, o mercado pode estar supervalorizado, tornando o aluguel mais vantajoso no curto prazo.
    
    4. **Taxas de juros**: Mudanças nas taxas de juros podem afetar tanto o financiamento quanto o rendimento dos investimentos.
    
    5. **Aspectos emocionais**: O sentimento de propriedade e segurança que um imóvel próprio proporciona não pode ser quantificado financeiramente.
    
    6. **Custos adicionais**: Impostos, manutenção, condomínio e reformas são custos que proprietários precisam considerar.
    
    7. **Liquidez patrimonial**: Imóveis têm baixa liquidez comparados a investimentos financeiros.
    """)

# Rodapé
st.markdown("---")
st.markdown("Simulador de Opções Imobiliárias | Desenvolvido por Manus AI | 2025")
