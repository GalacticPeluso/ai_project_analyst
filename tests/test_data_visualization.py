import unittest
import pandas as pd
import plotly.graph_objs as go
from src.data_visualization import plot_co2_emissions_over_time

class TestDataVisualization(unittest.TestCase):
    
    def setUp(self):
        # Crear un DataFrame de prueba
        self.df = pd.DataFrame({
            'region': ['A', 'B', 'C', 'D', 'E'],
            '2018': [100, 200, 300, 400, 500],
            '2019': [110, 210, 310, 410, 510],
            '2020': [120, 220, 320, 420, 520]
        })
    
    def test_plot_co2_emissions_over_time(self):
        fig = plot_co2_emissions_over_time(self.df)
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 5)  # Debería haber 5 líneas (una por cada región)

if __name__ == '__main__':
    unittest.main()

