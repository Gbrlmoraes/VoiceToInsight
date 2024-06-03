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

# Criando colunas onde ficarão os Cards
#col1, col2 = st.columns([4, 1])

# Criando dataframe com a quantidade por status
df_status = pd.DataFrame(df['status'].value_counts()).reset_index()
df_status.columns = ['Status', 'Quantidade']
df_status['cor'] = df_status['Status'].map({'Detrator' : '#EE4E4E', 'Neutro' : '#F6EEC9', 'Promotor' : '#A1DD70'})

# Criando gráfico de barras com streamlit
st.bar_chart(
    data = df_status,
    x = 'Status',
    y = 'Quantidade',
    color = 'cor',
    width = 12
    )

# Criar o gráfico de rosca
fig = px.pie(
    df_status, 
    values = 'Quantidade',
    names = 'Status',
    hole = 0.5,
    color_discrete_sequence = ['#A1DD70', '#F6EEC9' , '#EE4E4E'],
    category_orders = {"Status": ["Promotor", "Neutro", "Detrator"]}
)
st.plotly_chart(fig)