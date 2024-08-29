# Importing packages
import streamlit as st
import os

os.chdir('/home/gbrlmoraes/git_reps/VoiceToInsight')

# Page config
st.set_page_config(
    page_title = "VoiceToInsight",
    page_icon = "🎧",
)

# Title
st.title("VoiceToInsight🎧")
st.write("Plataforma de análise de NPS a partir de áudios")

st.image(
    "streamlit/images/home_image.jpg",
    caption = "Image designed by pikisuperstar / Freepik"
)
st.markdown(
    """
    Projeto feito com o objetivo de analisar os feedbacks coletados por chamada telefonica, e simplificar a obtenção e interpretação dos resultados de NPS.

    A solução foi desenvolvida como entrega do __Enterprise Challenge__, parte do curso de graduação em ciência de dados oferecido pela __[FIAP](https://www.fiap.com.br/)__, e tem o objetivo de resolver uma problemática proposta pela empresa __[TOTVS](https://www.totvs.com/)__.
    
    Desenvolvido por:
    - [Gabriel Moraes](https://www.linkedin.com/in/gabrielmoraesmagalhaes/)
    - [Yan Carrasco](https://www.linkedin.com/in/yan-carrasco/)
    - [Nicole Santos](https://www.linkedin.com/in/nicole-santos-906020245/)
    """
)