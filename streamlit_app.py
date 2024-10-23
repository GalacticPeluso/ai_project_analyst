import streamlit as st
import pandas as pd
import plotly.express as px
from github import Github
import io
import base64

# Configuración de la página
st.set_page_config(page_title="Análisis de Datos Agrícolas de Noruega", page_icon="🇳🇴", layout="wide")

# Función para cargar datos desde GitHub
@st.cache_data
def load_data_from_github(repo_name, file_path, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    file_content = repo.get_contents(file_path)
    decoded_content = base64.b64decode(file_content.content)
    df = pd.read_csv(io.StringIO(decoded_content.decode('utf-8')), sep=';', decimal=',')
    return df

# Título de la aplicación
st.title("Análisis de Datos de Producción y Subsidios Agrícolas de Noruega")

# Carga de datos
token = st.secrets["github"]["token"]
repo_name = "LandbruksdirektoratetGIT/opendata"
years = range(2017, 2025)
data = {}

for year in years:
    file_path = f"datasets/produksjon-og-avlosertilskudd/{year}/dataset.csv"
    try:
        data[year] = load_data_from_github(repo_name, file_path, token)
        st.success(f"Datos cargados para el año {year}")
    except Exception as e:
        st.error(f"Error al cargar datos para el año {year}: {e}")

# Selección de año
selected_year = st.selectbox("Seleccione un año", list(data.keys()))

if selected_year in data:
    df = data[selected_year]
    
    # Visualización de datos
    st.subheader(f"Datos para el año {selected_year}")
    
    # Selección de columnas numéricas
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    selected_column = st.selectbox("Seleccione una columna para visualizar", numeric_columns)
    
    # Gráfico de barras
    fig = px.bar(df, y=selected_column, title=f"Distribución de {selected_column}")
    st.plotly_chart(fig)
    
    # Estadísticas descriptivas
    st.subheader("Estadísticas Descriptivas")
    st.write(df[selected_column].describe())
    
    # Mapa de calor de correlaciones
    st.subheader("Mapa de Calor de Correlaciones")
    corr = df[numeric_columns].corr()
    fig_heatmap = px.imshow(corr, text_auto=True, aspect="auto")
    st.plotly_chart(fig_heatmap)

# Sección de preguntas y respuestas
st.subheader("Preguntas sobre los datos")
user_question = st.text_input("Haga una pregunta sobre los datos")
if user_question:
    # Aquí iría la lógica para responder preguntas
    st.write("Funcionalidad de respuesta a preguntas en desarrollo.")

# Pie de página
st.markdown("---")
st.markdown("Desarrollado con ❤️ usando Streamlit")

