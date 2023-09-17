import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
import tkinter as tk
from tkinter import filedialog

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

# Definir una función para actualizar la visualización
def update_visualization():
    global coordinates_file, depth_image_file, z_min, z_max

    # Cargar coordenadas y profundidad desde los archivos
    coordinates = load_coordinates_from_txt(coordinates_file)
    depth_image = load_depth_image(depth_image_file)

    x = coordinates[:, 0]
    y = coordinates[:, 1]

    z = []
    x1 = []
    y1 = []
    for coord_x, coord_y in zip(x, y):
        z1 = depth_image[int(coord_y), int(coord_x)]
        if z_min <= z1 <= z_max:
            z.append(z1)
            x1.append(coord_x)
            y1.append(coord_y)
    z = np.array(z)
    x1 = np.array(x1)
    y1 = np.array(y1)

    c3d = np.array([x1.tolist(), y1.tolist(), z.tolist()])
    c3d = c3d.T

    triangulation = Delaunay(c3d[:, 0:2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(c3d[:, 0], c3d[:, 1], c3d[:, 2], c='b', marker='o', label='Puntos')

    tetra_faces = c3d[triangulation.simplices]
    ax.add_collection3d(Poly3DCollection(tetra_faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.5))

    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    ax.set_title('Triangulación de Delaunay en 3D')
    plt.show()

# Función para seleccionar el archivo de coordenadas
def select_coordinates_file():
    global coordinates_file
    coordinates_file = filedialog.askopenfilename()

# Función para seleccionar el archivo de imagen de profundidad
def select_depth_image_file():
    global depth_image_file
    depth_image_file = filedialog.askopenfilename()

# Función para aplicar los cambios del rango de z
def apply_z_range():
    global z_min, z_max
    z_min = float(min_z_entry.get())
    z_max = float(max_z_entry.get())

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Visualización 3D")

# Configurar la interfaz para que ocupe todo el ancho y alto de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Crear un frame para los botones en el lado derecho
button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Agregar botones para seleccionar archivos
coordinates_button = tk.Button(button_frame, text="Seleccionar archivo de coordenadas", command=select_coordinates_file)
coordinates_button.pack()

depth_image_button = tk.Button(button_frame, text="Seleccionar archivo de imagen de profundidad", command=select_depth_image_file)
depth_image_button.pack()

# Agregar controles para ajustar el rango de z
min_z_label = tk.Label(button_frame, text="Valor mínimo de z:")
min_z_label.pack()

min_z_entry = tk.Entry(button_frame)
min_z_entry.pack()

max_z_label = tk.Label(button_frame, text="Valor máximo de z:")
max_z_label.pack()

max_z_entry = tk.Entry(button_frame)
max_z_entry.pack()

apply_button = tk.Button(button_frame, text="Aplicar Cambios de Rango", command=apply_z_range)
apply_button.pack()

# Agregar botón para actualizar visualización
update_button = tk.Button(button_frame, text="Actualizar Visualización", command=update_visualization)
update_button.pack()

# Ejecutar el bucle principal de la interfaz gráfica
root.mainloop()
