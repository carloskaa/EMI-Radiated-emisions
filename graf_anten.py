import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
file_path = 'Lindgren2.csv'  # Cambia esto si el archivo está en otra ubicación
data = pd.read_csv(file_path)

# Convertir las columnas a formato numérico, reemplazando comas por puntos
data['x'] = data['x'].str.replace(',', '.').astype(float)
data['Curve1'] = data['Curve1'].str.replace(',', '.').astype(float)

# Configurar la gráfica
plt.figure(figsize=(8, 6))
plt.plot(data['x'], data['Curve1'], marker='o', linestyle='-', color='b', label='Curve1')

# Etiquetas y título
plt.title('Gráfico de Curve1 vs x', fontsize=14)
plt.xlabel('x', fontsize=12)
plt.ylabel('Curve1', fontsize=12)
plt.legend()
plt.grid(True)
# plt.xscale('log')
# Mostrar la gráfica
plt.show()


data.to_csv('anten_med4.csv', index=False)