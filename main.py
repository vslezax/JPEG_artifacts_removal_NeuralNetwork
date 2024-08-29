from PIL import Image
import numpy as np
from scipy.ndimage import sobel, gaussian_filter

L = 8

def find_line_coefficients(x1, y1, x2, y2):
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    return k, b

def image_normalization(image_array):
    x1 = 65; y1 = 40
    x2 = 180; y2 = 210

    # y = kx + b
    c = np.zeros(256, dtype=np.float64)
    k, b = find_line_coefficients(0, 0, x1, y1)
    for i in range(x1):
        c[i] = k * i + b

    # Второе преобразование: от x1 до x2
    k, b = find_line_coefficients(x1, y1, x2, y2)
    for i in range(x1, x2):
        c[i] = k * i + b

    # Третье преобразование: от x2 до 255
    k, b = find_line_coefficients(x2, y2, 2 ** L - 1, 2 ** L - 1)
    for i in range(x2, 2 ** L):
        c[i] = k * i + b
    c = np.clip(c, 0, 255)

    normalized_array = np.copy(image_array)
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            normalized_array[i, j] = c[image_array[i, j]]

    return normalized_array

def image_denormalization(image_array):
    x1 = 40; y1 = 65
    x2 = 210; y2 = 180

    # y = kx + b
    c = np.zeros(256, dtype=np.float64)
    k, b = find_line_coefficients(0, 0, x1, y1)
    for i in range(x1):
        c[i] = k * i + b

    # Второе преобразование: от x1 до x2
    k, b = find_line_coefficients(x1, y1, x2, y2)
    for i in range(x1, x2):
        c[i] = k * i + b

    # Третье преобразование: от x2 до 255
    k, b = find_line_coefficients(x2, y2, 2 ** L - 1, 2 ** L - 1)
    for i in range(x2, 2 ** L):
        c[i] = k * i + b
    c = np.clip(c, 0, 255)

    normalized_array = np.copy(image_array)
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            normalized_array[i, j] = c[image_array[i, j]]

    return normalized_array


def sharpen_image(image_array, alpha):
    sobel_x = sobel(image_array, mode='constant', cval=0.0, axis=0)
    sobel_y = sobel(image_array, mode='constant', cval=0.0, axis=1)

    # Вычисляем градиент изображения
    magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

    # Создаем фильтр для увеличения резкости
    sharpened_array = image_array + alpha * magnitude

    # Убедимся, что значения в пределах [0, 255]
    sharpened_array = np.clip(sharpened_array, 0, 255)

    return sharpened_array

# Пример использования
import_path = 'E:/Загрузки/kodim1.jpg'
output_path = 'E:/Загрузки/'
image = Image.open(import_path).convert('L')
image_array = np.array(image)

# Linear enhancement
enhanced_image_array = image_normalization(image_array); image = Image.fromarray(np.uint8(enhanced_image_array)); image.save(output_path + 'enhanced.bmp')
filtered_image_array = gaussian_filter(enhanced_image_array, sigma=1.0); image = Image.fromarray(np.uint8(filtered_image_array)); image.save(output_path + 'filtered.bmp')
sharpen_image_array = sharpen_image(filtered_image_array, 0.5); image = Image.fromarray(np.uint8(sharpen_image_array)); image.save(output_path + 'sharpen.bmp')
deenhanced_image_array = image_denormalization(np.uint8(sharpen_image_array))

filtered_image = Image.fromarray(np.uint8(deenhanced_image_array))
filtered_image.save(output_path + 'export.bmp')
