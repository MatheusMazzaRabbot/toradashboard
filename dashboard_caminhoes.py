
import streamlit as st
import pandas as pd
import numpy as np
import seab as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🚚 Dashboard de Permanência de Caminhões nos Pátios")

# Dados fictícios
patios = ['12', '13', '14', '70', '60', 'Prada', 'CSN', 'Magnesia Importação', 
          'Magnesia Nacional', 'Manutenção', 'Carregamento']
tempos_medios = [3.5, 4.2, 2.8, 6.0, 5.1, 4.8, 3.7, 7.2, 6.5, 8.0, 5.5]
df_base = pd.DataFrame({'Pátio': patios, 'Tempo Médio (h)': tempos_medios})

# Heatmap por turno
turnos = ['Manhã', 'Tarde', 'Noite']
data_heatmap = []
for i, patio in enumerate(patios):
    for turno in turnos:
        tempo = max(0, tempos_medios[i] + np.random.uniform(-0.8, 0.8))
        data_heatmap.append({'Pátio': patio, 'Turno': turno, 'Tempo Médio (h)': tempo})
df_heatmap = pd.DataFrame(data_heatmap)

# Dispersão por caminhão
data_disp = []
for i, patio in enumerate(patios):
    tempos = np.random.normal(loc=tempos_medios[i], scale=0.8, size=100)
    tempos = np.clip(tempos, 0, None)
    for tempo in tempos:
        data_disp.append({'Pátio': patio, 'Tempo (h)': tempo})
df_dispersao = pd.DataFrame(data_disp)

# Tendência por dia
datas = [datetime.today() - timedelta(days=i) for i in range(29, -1, -1)]
data_tendencia = []
for i, patio in enumerate(patios):
    for data in datas:
        tempo = max(0, tempos_medios[i] + np.random.normal(0, 0.6))
        data_tendencia.append({'Data': data, 'Pátio': patio, 'Tempo (h)': tempo})
df_tendencia = pd.DataFrame(data_tendencia)

# Gráfico 1 - Tempo Médio
st.subheader("⏱️ Tempo Médio por Pátio")
fig1, ax1 = plt.subplots(figsize=(10, 6))
df_sorted = df_base.sort_values("Tempo Médio (h)")
cores = ['#440154' if t > df_base['Tempo Médio (h)'].mean() else '#21918c' for t in df_sorted['Tempo Médio (h)']]
bars = ax1.barh(df_sorted['Pátio'], df_sorted['Tempo Médio (h)'], color=cores)
ax1.axvline(df_base['Tempo Médio (h)'].mean(), color='gray', linestyle='--', label='Média Geral')
ax1.legend()
ax1.grid(axis='x', linestyle='--', alpha=0.6)
st.pyplot(fig1)

# Gráfico 2 - Heatmap por turno
st.subheader("🔥 Tempo Médio por Turno e Pátio")
df_pivot = df_heatmap.pivot(index='Pátio', columns='Turno', values='Tempo Médio (h)')
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.heatmap(df_pivot, annot=True, cmap="YlGnBu", fmt=".1f", ax=ax2)
st.pyplot(fig2)

# Gráfico 3 - Dispersão
st.subheader("📦 Dispersão dos Tempos por Pátio")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_dispersao, x='Tempo (h)', y='Pátio', palette='viridis', ax=ax3)
ax3.grid(axis='x', linestyle='--', alpha=0.6)
st.pyplot(fig3)

# Gráfico 4 - Tendência
st.subheader("📈 Tendência Diária por Pátio")
fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_tendencia, x='Data', y='Tempo (h)', hue='Pátio', ax=ax4)
ax4.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig4)

st.markdown("---")
st.caption("Modelo de painel interativo gerado com dados fictícios")
