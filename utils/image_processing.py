import numpy as np
from PIL import Image

def preprocess_image(image):
    """
    Pré-processa a imagem para o formato esperado pelo modelo
    """
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0).astype(np.float32)
    return image_array 