import streamlit as st
import logging
import pandas as pd
from googletrans import Translator
from src.data_agent import DataAgent
from src.data_visualization import (plot_bar_chart, plot_box_chart, plot_scatter_chart, 
                                    plot_stacked_bar_chart, plot_radar_chart, plot_animal_trends,
                                    plot_animal_distribution, plot_animal_heatmap)
import io

print("Iniciando la aplicación...")

# Configuración de la página
st.set_page_config(page_title="Análisis de Datos de Producción y Subsidios Agrícolas de Noruega", page_icon="🇳🇴", layout="wide")

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log_stream = io.StringIO()
logging.getLogger().addHandler(logging.StreamHandler(log_stream))

# Inicializar el traductor
translator = Translator()

# Traducciones pre-definidas
TRANSLATIONS = {
    "Análisis de Datos de Producción y Subsidios Agrícolas de Noruega": "Análisis de Datos de Producción y Subsidios Agrícolas de Noruega",
    "Seleccione un año": "Seleccione un año",
    "Visualizaciones": "Visualizaciones",
    "Gráfico de barras": "Gráfico de barras",
    "Gráfico de caja": "Gráfico de caja",
    "Gráfico de dispersión": "Gráfico de dispersión",
    "Gráfico de barras apiladas": "Gráfico de barras apiladas",
    "Gráfico de radar": "Gráfico de radar",
    "Seleccione una variable": "Seleccione una variable",
    "Seleccione una variable para el eje X": "Seleccione una variable para el eje X",
    "Seleccione una variable para el eje Y": "Seleccione una variable para el eje Y",
    "Tendencias significativas": "Tendencias significativas",
    "No se encontraron tendencias significativas.": "No se encontraron tendencias significativas.",
    "Tendencias de animales": "Tendencias de animales",
    "Seleccione animales para ver tendencias": "Seleccione animales para ver tendencias",
    "Preguntas sobre los datos": "Preguntas sobre los datos",
    "Haga una pregunta sobre los datos": "Haga una pregunta sobre los datos",
    "Respuesta:": "Respuesta:",
    "Distribución de animales": "Distribución de animales",
    "Mapa de calor de correlaciones": "Mapa de calor de correlaciones",
    "Análisis de Tendencias": "Análisis de Tendencias",
}

def translate_text(text):
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    try:
        return translator.translate(text, dest='es').text
    except:
        return text

@st.cache_data
def load_data():
    with st.spinner('Cargando datos...'):
        agent = DataAgent()
        files = agent.list_csv_and_readme_files()
        all_data = {}
        animal_codes = {}
        progress_bar = st.progress(0)
        for i, file_info in enumerate(files):
            year = file_info['year']
            data = agent.load_csv(file_info['dataset'])
            readme_content = agent.load_readme(file_info['readme'])
            if data is not None:
                all_data[year] = data
            if readme_content is not None:
                animal_codes.update(agent.extract_animal_codes(readme_content))
            progress_bar.progress((i + 1) / len(files))
    return all_data, animal_codes

def main():
    print("Entrando en la función main()")
    st.title(translate_text("Análisis de Datos de Producción y Subsidios Agrícolas de Noruega"))

    all_data, animal_codes = load_data()

    if not all_data:
        st.error("No se pudieron cargar los datos. Por favor, verifica la conexión y los permisos.")
        return

    tab1, tab2, tab3 = st.tabs(["Visualizaciones", "Análisis de Tendencias", "Preguntas"])

    with tab1:
        st.header(translate_text("Visualizaciones"))
        years = list(all_data.keys())
        selected_year = st.selectbox(translate_text("Seleccione un año"), years)
        data = all_data[selected_year]

        chart_type = st.selectbox(translate_text("Seleccione un tipo de gráfico"), 
                                  ["Gráfico de barras", "Gráfico de caja", "Gráfico de dispersión", 
                                   "Gráfico de barras apiladas", "Gráfico de radar", 
                                   "Distribución de animales", "Mapa de calor de correlaciones"])

        if chart_type == "Gráfico de barras":
            variable = st.selectbox(translate_text("Seleccione una variable"), data.columns)
            fig = plot_bar_chart(data, variable)
            st.plotly_chart(fig)

        elif chart_type == "Gráfico de caja":
            variable = st.selectbox(translate_text("Seleccione una variable"), data.columns)
            fig = plot_box_chart(data, variable)
            st.plotly_chart(fig)

        elif chart_type == "Gráfico de dispersión":
            x_variable = st.selectbox(translate_text("Seleccione una variable para el eje X"), data.columns)
            y_variable = st.selectbox(translate_text("Seleccione una variable para el eje Y"), data.columns)
            fig = plot_scatter_chart(data, x_variable, y_variable)
            st.plotly_chart(fig)

        elif chart_type == "Gráfico de barras apiladas":
            variables = st.multiselect(translate_text("Seleccione variables"), data.columns)
            if variables:
                fig = plot_stacked_bar_chart(data, variables)
                st.plotly_chart(fig)

        elif chart_type == "Gráfico de radar":
            variables = st.multiselect(translate_text("Seleccione variables"), data.columns)
            if variables:
                fig = plot_radar_chart(data, variables)
                st.plotly_chart(fig)

        elif chart_type == "Distribución de animales":
            animal_columns = [col for col in data.columns if col in animal_codes]
            fig = plot_animal_distribution(data, animal_columns, animal_codes)
            st.plotly_chart(fig)

        elif chart_type == "Mapa de calor de correlaciones":
            animal_columns = [col for col in data.columns if col in animal_codes]
            fig = plot_animal_heatmap(data, animal_columns, animal_codes)
            st.plotly_chart(fig)

    with tab2:
        st.header(translate_text("Análisis de Tendencias"))
        agent = DataAgent()
        trends = agent.find_significant_trends(all_data)
        if trends:
            for animal_code, trend_info in trends.items():
                animal_name = animal_codes.get(animal_code, animal_code)
                st.write(f"{animal_name} ({animal_code}): Tendencia {trend_info['direction']}")
                st.write(f"- p-value: {trend_info['p_value']:.4f}")
                st.write(f"- R^2: {trend_info['r_squared']:.4f}")
                st.write(f"- Pendiente: {trend_info['slope']:.4f}")
                st.write(f"- Intercepto: {trend_info['intercept']:.4f}")
                st.write(f"- Descripción: {trend_info['description']}")
                st.write("---")
        else:
            st.write(translate_text("No se encontraron tendencias significativas."))
        
        st.subheader(translate_text("Tendencias de animales"))
        animal_trends = agent.calculate_animal_trends(all_data)
        selected_animals = st.multiselect(translate_text("Seleccione animales para ver tendencias"), 
                                          options=[(code, animal_codes.get(code, code)) for code in animal_trends.keys()],
                                          format_func=lambda x: f"{x[1]} ({x[0]})")
        if selected_animals:
            trend_data = {animal[0]: trends for animal, trends in animal_trends.items() if animal in selected_animals}
            fig = plot_animal_trends(trend_data, animal_codes)
            st.plotly_chart(fig)

    with tab3:
        st.header(translate_text("Preguntas sobre los datos"))
        user_question = st.text_input(translate_text("Haga una pregunta sobre los datos"))
        if user_question:
            answer = agent.answer_question(data, user_question)
            st.write(translate_text("Respuesta:"), answer)

if __name__ == "__main__":
    print("Llamando a main()")
    main()

