import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_bar_chart(data, variable):
    fig = px.bar(data, x=data.index, y=variable, title=f'Gráfico de barras de {variable}')
    return fig

def plot_box_chart(data, variable):
    fig = px.box(data, y=variable, title=f'Gráfico de caja de {variable}')
    return fig

def plot_scatter_chart(data, x_variable, y_variable):
    fig = px.scatter(data, x=x_variable, y=y_variable, title=f'Gráfico de dispersión de {x_variable} vs {y_variable}')
    return fig

def plot_stacked_bar_chart(data, variables):
    fig = go.Figure()
    for variable in variables:
        fig.add_trace(go.Bar(x=data.index, y=data[variable], name=variable))
    fig.update_layout(barmode='stack', title='Gráfico de barras apiladas')
    return fig

def plot_radar_chart(data, variables):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[data[var].mean() for var in variables],
        theta=variables,
        fill='toself'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        title='Gráfico de radar'
    )
    return fig

def plot_animal_trends(trend_data, animal_codes):
    fig = go.Figure()
    for animal_code, trends in trend_data.items():
        animal_name = animal_codes.get(animal_code, animal_code)
        # Filtrar los valores nulos
        valid_years = [year for year, value in zip(trends['years'], trends['values']) if pd.notnull(value)]
        valid_values = [value for value in trends['values'] if pd.notnull(value)]
        if valid_years and valid_values:
            fig.add_trace(go.Scatter(x=valid_years, y=valid_values, mode='lines+markers', name=f"{animal_name} ({animal_code})"))
    fig.update_layout(title='Tendencias de animales', xaxis_title='Año', yaxis_title='Valor')
    return fig

def plot_animal_distribution(data, animal_columns, animal_codes):
    animal_data = data[animal_columns].mean().sort_values(ascending=False)
    animal_names = [f"{animal_codes.get(col, col)} ({col})" for col in animal_data.index]
    fig = px.bar(x=animal_names, y=animal_data.values, 
                 title="Distribución promedio de animales",
                 labels={'x': 'Animal', 'y': 'Promedio'})
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_animal_heatmap(data, animal_columns, animal_codes):
    corr_matrix = data[animal_columns].corr()
    animal_names = [f"{animal_codes.get(col, col)} ({col})" for col in corr_matrix.index]
    fig = px.imshow(corr_matrix, 
                    x=animal_names, 
                    y=animal_names,
                    color_continuous_scale="RdBu_r",
                    title="Mapa de calor de correlaciones entre animales")
    fig.update_layout(xaxis_tickangle=-45)
    return fig