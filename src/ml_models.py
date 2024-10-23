from sklearn.cluster import KMeans

def analyze_emissions(df):
    """
    Realiza un análisis de clustering de las emisiones.
    """
    # Seleccionar características para el clustering
    X = df[['co2', 'nox']]
    
    # Realizar clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)
    
    # Calcular estadísticas por cluster
    cluster_stats = df.groupby('cluster').agg({
        'co2': 'mean',
        'nox': 'mean',
        'merke': lambda x: x.value_counts().index[0]  # marca más común en el cluster
    }).reset_index()
    
    cluster_stats.columns = ['Cluster', 'CO2 Promedio', 'NOx Promedio', 'Marca más común']
    
    return cluster_stats

# ... (mantener las funciones existentes)

