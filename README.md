# Análisis de Datos Agrícolas de Noruega

Este proyecto proporciona una interfaz web para analizar datos agrícolas de Noruega, utilizando datos del repositorio LandbruksdirektoratetGIT/opendata en GitHub.

## Características

- Carga y visualización de datos CSV del repositorio de GitHub.
- Interfaz de consulta para analizar los datos cargados.
- Soporte multilingüe (Español, English, Norsk, Français, Deutsch).
- Visualizaciones interactivas de los datos.

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación Streamlit.
- `src/data_agent.py`: Contiene la lógica principal para el análisis de datos.
- `src/repo_analysis.py`: Funciones para analizar el contenido del repositorio de GitHub.

## Configuración

1. Clona este repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Configura tus credenciales de GitHub en `.streamlit/secrets.toml`:
   ```toml
   github_access_token = "tu_token_de_github"
   ```

## Uso

Ejecuta la aplicación con:

