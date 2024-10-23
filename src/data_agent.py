import streamlit as st
from github import Github
import pandas as pd
import numpy as np
from scipy import stats
import requests
import io
import logging
import traceback
import re

class DataAgent:
    def __init__(self):
        self.github_token = st.secrets["github"]["token"]
        self.repo_name = st.secrets["github"]["repo"]
        self.base_url = f"https://raw.githubusercontent.com/{self.repo_name}/main/"
        self.data_directory = "datasets/produksjon-og-avlosertilskudd"
        logging.info(f"DataAgent inicializado con repo: {self.repo_name}")

    def list_csv_and_readme_files(self):
        logging.info("Iniciando listado de archivos CSV y README")
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(self.data_directory)
        
        files = []
        for content in contents:
            if content.type == "dir":
                year = content.name
                year_contents = repo.get_contents(content.path)
                csv_file = next((f for f in year_contents if f.name.endswith('.csv')), None)
                readme_file = next((f for f in year_contents if f.name.lower() == 'readme.md'), None)
                
                if csv_file and readme_file:
                    files.append({
                        'year': year,
                        'dataset': csv_file.download_url,
                        'readme': readme_file.download_url
                    })
                    logging.info(f"Archivos encontrados para el año {year}")
                else:
                    logging.warning(f"No se encontraron archivos CSV o README para el año {year}")
        
        logging.info(f"Total de años procesados: {len(files)}")
        return files

    def load_readme(self, url):
        logging.info(f"Intentando cargar README desde: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            logging.info(f"README cargado exitosamente, longitud: {len(content)}")
            return content
        except Exception as e:
            logging.error(f"Error al cargar el README: {str(e)}")
            return None

    def load_csv(self, url):
        logging.info(f"Intentando cargar CSV desde: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.content.decode('utf-8')
            df = pd.read_csv(io.StringIO(content), sep=';', decimal=',')
            
            # Convertir columnas numéricas a float, manejando valores vacíos
            numeric_columns = df.select_dtypes(include=['object']).columns
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col].str.replace(',', '.'), errors='coerce')
            
            logging.info(f"CSV cargado exitosamente, shape: {df.shape}")
            return df
        except Exception as e:
            logging.error(f"Error al cargar el CSV: {str(e)}")
            logging.error(traceback.format_exc())
            return None

    def extract_animal_codes(self, readme_content):
        animal_codes = {}
        pattern = r'(\d+)\s*=\s*(.+)'
        matches = re.findall(pattern, readme_content)
        for code, name in matches:
            animal_codes[code] = name.strip()
        return animal_codes

    def find_significant_trends(self, all_data):
        trends = {}
        years = sorted(all_data.keys())
        
        # Encontrar columnas comunes en todos los años
        common_columns = set(all_data[years[0]].columns)
        for year in years[1:]:
            common_columns = common_columns.intersection(set(all_data[year].columns))
        
        for column in common_columns:
            try:
                values = [all_data[year][column].mean() for year in years]
                slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(years)), values)
                if p_value < 0.05:  # Consideramos tendencias significativas si p < 0.05
                    direction = "creciente" if slope > 0 else "decreciente"
                    trends[column] = {
                        "direction": direction,
                        "p_value": p_value,
                        "r_squared": r_value**2,
                        "slope": slope,
                        "intercept": intercept,
                        "description": self.describe_trend(slope, r_value**2)
                    }
            except Exception as e:
                logging.warning(f"No se pudo calcular la tendencia para la columna {column}: {str(e)}")

        return trends

    def describe_trend(self, slope, r_squared):
        strength = "fuerte" if r_squared > 0.7 else "moderada" if r_squared > 0.5 else "débil"
        speed = "rápida" if abs(slope) > 1 else "moderada" if abs(slope) > 0.5 else "lenta"
        return f"Tendencia {strength} y {speed}"

    def calculate_animal_trends(self, all_data):
        animal_trends = {}
        years = sorted(all_data.keys())
        
        # Encontrar columnas comunes en todos los años
        common_columns = set(all_data[years[0]].columns)
        for year in years[1:]:
            common_columns = common_columns.intersection(set(all_data[year].columns))
    
        for column in common_columns:
            try:
                values = [all_data[year][column].mean() for year in years]
                animal_trends[column] = {
                    "years": years,
                    "values": values
                }
            except Exception as e:
                logging.warning(f"No se pudo calcular la tendencia para la columna {column}: {str(e)}")
    
        return animal_trends

    def answer_question(self, data, question):
        logging.info(f"Recibida pregunta: {question}")
        # Implementa esta función para responder preguntas sobre los datos
        # Por ahora, retornamos una respuesta genérica
        logging.info("Respuesta genérica enviada")
        return "Lo siento, aún no puedo responder a preguntas específicas sobre los datos."