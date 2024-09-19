import cv2 #pip install opencv-python pyembroidery
import numpy as np
from pyembroidery import EmbPattern, STITCH, JUMP, write_dst #pip install pyembroidery

# Paso 1: Carga la imagen jpg y la convierte a escalas grises
def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")
    return image

# Paso 2: Detecta los bordes usando Canny
def detec_edges(image):
    edges = cv2.Canny(image, 50, 150) # ajusta los umbrales para controlar los bordes
    return edges

# Paso 3: Encontrar contornos y filtrar los mas pequeños
def find_contours(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Filtrar contornos pequeños
    contours =[c for c in contours if cv2.contourArea(c) > 100] # Aqui se ajusta el valor de 100 segun sea necesario
    return contours

# Paso 4: Convierte los entornos en un archivo de bordado (DST)
def contours_to_embroidery(contours, output_file):
    pattern = EmbPattern()
    for contour in contours:
        if len(contour) > 5: #filtra contornos pequeños
            for i, point in enumerate(contour):
                x, y = point[0]
                if  i == 0:
                    pattern.add_stitch_absolute(JUMP, x, y)
                else:
                    pattern.add_stitch_absolute(STITCH, x, y)
    pattern.add_stitch_absolute(STITCH, 0, 0)
    write_dst(pattern, output_file)

# Paso 5: Muestra la imagen procesada al finalizar el proceso
def display_image(image, window_name="Image"):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Funcion principal
def convert_jpg_to_dst(jpg_file, dst_output):
    image = load_and_preprocess_image(jpg_file)
    edges = detec_edges(image)
    display_image(edges, "Detected Edge")
    contours = find_contours(edges)
    contours_to_embroidery(contours, dst_output)
    print(f"Conversion completa: archivos DST guardado en {dst_output}")

# Ejecuta el programa
if __name__ == "__main__":
    jpg_file = 'C:/Users/on.jpg' # Carga la ubicacion de la imagen jpg
    dst_output = 'nuevo.dst' # Da el nombre al archivo nuevo
    convert_jpg_to_dst(jpg_file, dst_output)
