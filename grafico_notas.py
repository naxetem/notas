import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

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
#st.subheader("Distribución de puntuaciones")
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
#Ocultado para evitar problemas de visualización
#st.plotly_chart(fig)



# Posición según puntuación
st.subheader("Calcular posición de una nota")

# Campos para Teoría
st.write("Teoría")
aciertos_teoria = st.number_input("Aciertos Teoría:", min_value=0,max_value=80, step=1, value=0)
fallos_teoria = st.number_input("Fallos Teoría:", min_value=0,max_value=80, step=1, value=0)
nc_teoria = st.number_input("NC Teoría:", min_value=0, step=1,max_value=80, value=0)

# Campos para Práctica
st.write("Práctica")
aciertos_practica = st.number_input("Aciertos Práctica:", min_value=0,max_value=20,step=1, value=0)
fallos_practica = st.number_input("Fallos Práctica:", min_value=0, max_value=20,step=1, value=0)
nc_practica = st.number_input("NC Práctica:", min_value=0,max_value=20, step=1, value=0)

# Convertir los valores a float para mayor precisión
aciertos_teoria = float(aciertos_teoria)
fallos_teoria = float(fallos_teoria)
aciertos_practica = float(aciertos_practica)
fallos_practica = float(fallos_practica)

# Calcular notas con precisión
nota_teoria = aciertos_teoria - (1/3) * fallos_teoria
nota_practica = 4 * aciertos_practica - (4/3) * fallos_practica
nota_total = nota_teoria + nota_practica

st.write(f"Nota Teoría: {nota_teoria:.2f}")
st.write(f"Nota Práctica: {nota_practica:.2f}")
st.write(f"Nota Total: {nota_total:.2f}")


# Calcular posición automáticamente al cambiar la nota
try:
    filtrado = df_filtered[df_filtered["Puntuacion total directa"] <= nota_total]
    if not filtrado.empty:
        posicion = filtrado.iloc[0]["orden"]
        st.write(f"Posición: **{posicion}**")
    else:
        st.write("No se encontró una posición para la nota ingresada.")
except Exception as e:
    st.write(f"Error al calcular la posición: {e}")

# Añadir un marcador al gráfico para la nota total
fig.add_trace(go.Scatter(x=[nota_total], y=[0], mode='markers+text', text=['Nota Total'], textposition='top center', marker=dict(color='red', size=10), name='Nota Total'))

# Mostrar el gráfico actualizado
st.plotly_chart(fig)