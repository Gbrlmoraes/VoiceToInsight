import streamlit as st

# Título da página
st.title("Página de Pagamento 💵")

# Informações dos planos
st.header("Escolha seu plano de asinatura:")
plans = {
    "Básico": {"Preço": 300, "Limite": 100},
    "Avançado": {"Preço": 700, "Limite": 500},
    "Premium": {"Preço": 1500, "Limite": 2000}
}

# Seleção do plano
selected_plan = st.selectbox("Selecione o plano", options=list(plans.keys()))

# Mostrar detalhes do plano selecionado
plan_price = plans[selected_plan]["Preço"]
plan_limit = plans[selected_plan]["Limite"]
st.write(f"**Plano {selected_plan}:** R$ {plan_price}/mês (até {plan_limit} áudios)")

# Input para quantidade de áudios
num_audios = st.number_input("Quantos áudios deseja processar por mês?", min_value=0, value=plan_limit)

# Calcular o custo adicional, se houver
if num_audios > plan_limit:
    extra_audios = num_audios - plan_limit
    extra_cost = extra_audios * 2  # R$ 2 por áudio excedente
else:
    extra_audios = 0
    extra_cost = 0

# Mostrar o custo total
total_cost = plan_price + extra_cost
st.write(f"Áudios excedentes: {extra_audios} (R$ {extra_cost})")
st.write(f"**Custo Total: R$ {total_cost}/mês**")

# Botão de pagamento
if st.button("Concluir Pagamento"):
    st.success(f"Pagamento concluído! Você selecionou o plano {selected_plan} e o total a ser pago é R$ {total_cost}/mês.")
