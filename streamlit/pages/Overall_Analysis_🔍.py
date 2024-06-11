# Bibliotecas que foram usadas
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title = "Overall",
    page_icon = "🔍",
)

st.title('Overall Analysis')

# Import dos dados
st.cache_data()
def load_data():
    return pd.read_csv(r'J:\Estudo\Projetos\VoiceToInsight\data\nps_data.csv')

df = load_data()

### Notas Gerais de NPS
st.subheader('Notas de NPS')

col1, col2, col3 = st.columns(3)
with col1:
    nota = round(df['nps_atendimento'].mean(), 2)
    st.metric('NPS Atendimento', nota, delta = round(nota - 8, 2))
with col2:
    nota = round(df['nps_suporte_tecnico'].mean(), 2)
    st.metric('NPS Suporte Técnico', nota, delta = round(nota - 8, 2))
with col3:
    nota = round(df['nps_comercial_financeiro'].mean(), 2)
    st.metric('NPS Comercial/Financeiro', nota, delta = round(nota - 8, 2))

col1, col2, col3 = st.columns(3)
with col1:
    nota = round(df['nps_recomendacao'].mean(), 2)
    st.metric('NPS Recomendação', nota, delta = round(nota - 8, 2))
with col2:
    nota = round(df['nps_satisfacao'].mean(), 2)
    st.metric('NPS Satisfação', nota, delta = round(nota - 8, 2))
with col3:
    nota = round(df['nps_custo'].mean(), 2)
    st.metric('NPS Custo', nota, delta = round(nota - 8, 2))

col1, col2, col3 = st.columns(3)
with col1:
    nota = round(df['nps_unidade'].mean(), 2)
    st.metric('NPS Unidade', nota, delta = round(nota - 8, 2))
with col2:
    nota = round(df['nps_rh'].mean(), 2)
    st.metric('NPS RH', nota, delta = round(nota - 8, 2))
with col3:
    nota = round(df['nps_outros'].mean(), 2)
    st.metric('NPS Outros*', nota, delta = round(nota - 8, 2))

st.markdown('''
    \* _O valor da nota de NPS "Outros" corresponde à média das outras categorias de NPS que podem ter sido avaliadas em uma determinada pesquisa, mas que não se encaixam nas categorias principais._ \n
    \** _As variações abaixo das notas médias representam a pontuação excedente, ou faltante, para que se atinja o estado de promotor._     
''') 

### Análise por classificacao das avaliações de NPS

# Criando dataframe com a quantidade por status
df_status = pd.DataFrame(df['status'].value_counts()).reset_index()
df_status.columns = ['Status', 'Quantidade']
df_status['cor'] = df_status['Status'].map({'Detrator' : '#EE4E4E', 'Neutro' : '#F6EEC9', 'Promotor' : '#A1DD70'})

# Textos
st.subheader('Promotores e Detratores')

status_max = df_status[df_status['Quantidade'] == df_status['Quantidade'].max()]['Status'].values[0]
status_min = df_status[df_status['Quantidade'] == df_status['Quantidade'].min()]['Status'].values[0]

st.markdown(f'''
    Podemos ver que a maior parte das avaliações se encontra no status de __{status_max}__, já o status __{status_min}__, representa a menor parte das avaliações\n
''')
st.markdown('''
    <ul>
        <li><i><font color=#A1DD70>Promotor</font>: 8 -> 10</i></li>
        <li><i><font color=#F6EEC9>Neutro</font>: 6 -> 8</i></li>
        <li><i><font color=#EE4E4E>Detrator</font>: 0 -> 6</i></li>
    </ul>        
''', unsafe_allow_html = True)

# Criando gráfico de barras com streamlit
st.bar_chart(
    data = df_status,
    x = 'Status',
    y = 'Quantidade',
    color = 'cor',
    width = 12
)

### Análise do sucesso dos atendimentos

# Criando dataframe com a quantidade por sucesso do atendimento
df_atendimento = pd.DataFrame(df['atendimento'].value_counts()).reset_index()
df_atendimento.columns = ['Status', 'Quantidade']
df_atendimento['cor'] = df_status['Status'].map({'Não' : '#EE4E4E', 'Sim' : '#A1DD70'})

# Textos
st.subheader('Sucesso dos atendimentos')

st.write('O gráfico abaixo mostra a quantidade de atendimentos onde foi possível realizar a pesquisa de NPS (__<font color=#A1DD70>Sim</font>__), versus a quantidade de atendimentos que tiveram algum impedimento (__<font color=#EE4E4E>Não</font>__)', unsafe_allow_html = True)

# Criar o gráfico de rosca
fig = px.pie(
    df_atendimento, 
    values = 'Quantidade',
    names = 'Status',
    hole = 0.5,
    color_discrete_sequence = ['#A1DD70', '#EE4E4E'],
    category_orders = {"Status": ['Sim','Não']}
)
st.plotly_chart(fig)