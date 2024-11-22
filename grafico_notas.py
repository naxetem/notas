import pandas as pd
import plotly.express as px
import streamlit as st

# Configurar la página en modo "wide"
st.set_page_config(layout="wide")

# Cargar los datos
df_filtered = pd.read_csv("notas_disociadas.csv")

min_value = int(48)
max_value = int(140)

df_filtered['Intervalo'] = pd.cut(df_filtered['Puntuacion total directa'], bins=range(min_value, max_value + 1, 1), right=False)
interval_counts = df_filtered['Intervalo'].value_counts().sort_index()

# Convertir los intervalos a cadenas de texto
interval_counts.index = interval_counts.index.astype(str)

# Calcular la frecuencia acumulada
interval_counts_acumulada = interval_counts.iloc[::-1].cumsum().iloc[::-1]

# Interfaz de Streamlit
st.title("Gráficos y Posición de Puntuaciones TAI 2023")

# Convertir los intervalos a cadenas que muestran solo el límite inferior
interval_counts.index = [str(interval.left) for interval in df_filtered['Intervalo'].cat.categories]

# Gráfico de barras interactivo con etiquetas mejoradas
st.subheader("Distribución de puntuaciones")
fig = px.bar(
    interval_counts,
    labels={'index': 'Puntuación mínima del intervalo', 'value': 'Frecuencia'},
    title="Distribución de Puntuaciones",
    color_discrete_sequence=["#636EFA"],  # Color profesional
    text=interval_counts_acumulada.values  # Mostrar valores en las barras
)

# Mejoras al diseño
fig.update_layout(
    xaxis_title="Puntuación mínima del intervalo",
    yaxis_title="Frecuencia",
    title_font_size=20,
    title_font_family="Arial",
    title_x=0.5,
    xaxis=dict(tickangle=0),  # Alineación horizontal
    yaxis=dict(showgrid=True, gridcolor="lightgray"),  # Cuadrícula del eje Y
    plot_bgcolor="white",  # Fondo blanco
)

fig.update_traces(
    text=interval_counts_acumulada.values,  # Mostrar valores acumulados en las barras
    textposition='outside',  # Posición del texto fuera de las barras
    textfont=dict(
        size=30,  # Tamaño de la fuente del texto
        color='black',  # Color de la fuente del texto
        family='Arial'  # Familia de la fuente del texto
    ),
    marker=dict(
        color='blue',  # Color de los marcadores
        line=dict(
            color='black',  # Color del borde de los marcadores
            width=0  # Ancho del borde de los marcadores
        )
    ),
    hovertext="Frecuencia acumulada",
    opacity=0.8  # Opacidad de la traza
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)



# Posición según puntuación
st.subheader("Calcular posición de una nota")
nota = st.number_input("Introduce una puntuación sobre 160:", min_value=0.0, max_value=160.0, step=0.1, value=float(80), format="%.2f")

# Calcular posición automáticamente al cambiar la nota
try:
    filtrado = df_filtered[df_filtered["Puntuacion total directa"] <= nota]
    if not filtrado.empty:
        posicion = filtrado.iloc[0]["orden"]
        st.write(f"Posición: **{posicion}**")
    else:
        st.write("No se encontró una posición para la nota ingresada.")
except Exception as e:
    st.write(f"Error al calcular la posición: {e}")
