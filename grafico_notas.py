import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Cargar los datos
df_filtered = pd.read_csv("notas_disociadas.csv")

# Calcular intervalos
min_value = int(df_filtered['Puntuacion total directa'].min())
max_value = int(df_filtered['Puntuacion total directa'].max()) + 1

df_filtered['Intervalo'] = pd.cut(df_filtered['Puntuacion total directa'], bins=range(min_value, max_value + 1, 1), right=False)
interval_counts = df_filtered['Intervalo'].value_counts().sort_index()

# Interfaz de Streamlit
st.title("Gráficos y Posición de Puntuaciones TAI 2023")

# Gráfico de barras
st.subheader("Distribución de puntuaciones")
fig, ax = plt.subplots(figsize=(10, 6))
interval_counts.plot(kind='bar', ax=ax, color='blue', width=0.9)

# Ajustar etiquetas del eje X
intervals = interval_counts.index
labels = [str(interval.left) if i % 5 == 0 else '' for i, interval in enumerate(intervals)]
ax.set_xticklabels(labels, rotation=45)

ax.set_xlabel('Intervalo de Puntuación')
ax.set_ylabel('Frecuencia')
ax.set_title('Distribución de Puntuaciones en Intervalos de 1 Punto')
ax.grid(axis='y')
st.pyplot(fig)

# Posición según puntuación
st.subheader("Calcular posición de una nota")
nota = st.number_input("Introduce una puntuación:", min_value=0.0, max_value=160.0, step=0.1, format="%.2f")

# Calcular posición automáticamente al cambiar la nota
try:
    filtrado = df_filtered[df_filtered["Puntuacion total directa"] <= nota]
    if not filtrado.empty:
        posicion = filtrado.iloc[0]["orden"]
        st.write(f"La posición para la nota {nota:.2f} es: {posicion}")
    else:
        st.write("No se encontró una posición para la nota ingresada.")
except Exception as e:
    st.write(f"Error al calcular la posición: {e}")
