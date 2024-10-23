import streamlit as st
from github import Github
import pandas as pd
import io

def test_github_connection():
    # Acceder a los secretos
    github_token = st.secrets["github"]["token"]
    repo_name = st.secrets["github"]["repo"]

    # Inicializar el cliente de GitHub
    g = Github(github_token)

    try:
        # Intentar acceder al repositorio
        repo = g.get_repo(repo_name)
        print(f"Conexión exitosa al repositorio: {repo.full_name}")

        # Listar algunos contenidos del repositorio
        contents = repo.get_contents("datasets")
        print("\nContenido de la carpeta 'datasets':")
        for content in contents:
            print(f"- {content.path}")

        # Intentar cargar un archivo CSV como ejemplo
        csv_path = "datasets/foretak/dataset.csv"
        try:
            file_content = repo.get_contents(csv_path)
            df = pd.read_csv(io.StringIO(file_content.decoded_content.decode()))
            print(f"\nSe cargó exitosamente el archivo {csv_path}")
            print(f"Dimensiones del DataFrame: {df.shape}")
            print("\nPrimeras 5 filas del DataFrame:")
            print(df.head())
        except Exception as e:
            print(f"Error al cargar el archivo CSV {csv_path}: {str(e)}")
            print("Contenido del archivo:")
            print(file_content.decoded_content[:1000])  # Imprimir los primeros 1000 bytes del contenido

    except Exception as e:
        print(f"Error al acceder al repositorio: {str(e)}")

if __name__ == "__main__":
    test_github_connection()

