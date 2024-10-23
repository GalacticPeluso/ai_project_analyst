import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import streamlit as st

class DataAnalystVisualizer:
    def __init__(self):
        pass

    def analyze_and_visualize(self, df, question):
        # Generar una respuesta basada en la pregunta
        response = self.generate_response(df, question)

        # Extraer información clave de la respuesta
        column_to_visualize = self._extract_column(question, df.columns)
        
        if column_to_visualize:
            # Generar visualización
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if pd.api.types.is_numeric_dtype(df[column_to_visualize]):
                sns.histplot(df[column_to_visualize], ax=ax)
                ax.set_title(f"Distribución de {column_to_visualize}")
            else:
                df[column_to_visualize].value_counts().plot(kind='bar', ax=ax)
                ax.set_title(f"Conteo de {column_to_visualize}")
            
            ax.set_xlabel(column_to_visualize)
            ax.set_ylabel("Frecuencia")
            
            # Convertir el gráfico a una imagen
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            
            return response, f"data:image/png;base64,{plot_url}"
        else:
            return response, None

    def generate_response(self, df, question):
        question = question.lower()
        if "promedio" in question or "media" in question:
            column = self._extract_column(question, df.columns)
            if column:
                return f"El promedio de {column} es {df[column].mean():.2f}"
        elif "máximo" in question:
            column = self._extract_column(question, df.columns)
            if column:
                return f"El valor máximo de {column} es {df[column].max():.2f}"
        elif "mínimo" in question:
            column = self._extract_column(question, df.columns)
            if column:
                return f"El valor mínimo de {column} es {df[column].min():.2f}"
        elif "total" in question or "suma" in question:
            column = self._extract_column(question, df.columns)
            if column:
                return f"La suma total de {column} es {df[column].sum():.2f}"
        elif "cuántos" in question or "cantidad" in question:
            return f"El dataset contiene {len(df)} registros"
        elif "columnas" in question:
            return f"Las columnas del dataset son: {', '.join(df.columns)}"
        else:
            return "Lo siento, no puedo responder a esa pregunta en este momento."

    def _extract_column(self, text, columns):
        for col in columns:
            if col.lower() in text.lower():
                return col
        return None

