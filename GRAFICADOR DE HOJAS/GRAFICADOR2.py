import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Importar las bibliotecas necesarias

# Definir una función para cargar coordenadas desde un archivo txt
def load_coordinates_from_txt(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Omitir la primera línea
        for line in lines:
            x, y = map(float, line.strip().split())
            coordinates.append([x, y])
    return np.array(coordinates)

# Definir una función para cargar una imagen de profundidad npy
def load_depth_image(file_path):
    return np.load(file_path)

# Definir las rutas de los archivos a cargar
coordinates_file = 'coordenadas_hoja_10.txt'
depth_image_file = 'imagen_profundidad_12_redimensionada.npy'

# Cargar coordenadas y profundidad desde los archivos
coordinates = load_coordinates_from_txt(coordinates_file)
depth_image = load_depth_image(depth_image_file)

# Obtener las coordenadas x e y por separado
x = coordinates[:, 0]
y = coordinates[:, 1]

# Obtener la profundidad de la imagen para cada coordenada
z = []
for coord_x, coord_y in zip(x, y):
    z.append(depth_image[int(coord_y), int(coord_x)])
z = np.array(z)

# Crear una figura y un eje 3D utilizando matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Crear un gráfico de dispersión en 3D con las coordenadas x, y, z
ax.scatter(x, y, z, c='r', marker='o')

# Etiquetar los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Mostrar el gráfico
plt.show()
