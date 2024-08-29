import pandas as pd
import requests
import os

# Задайте путь к вашему CSV файлу
csv_file_path = 'path_to_your_csv_file.csv'

# Создаем директорию для сохранения изображения
output_dir = 'images_dataset'
os.makedirs(output_dir, exist_ok=True)

# Читаем CSV файл
df = pd.read_csv(csv_file_path, header=None)

# Получаем URL из первой строки и второго столбца
first_image_url = df.iloc[0, 1]  # Измените индекс [0, 1] если URL находится в другом столбце

# Извлекаем имя файла из URL
image_name = first_image_url.split('/')[-1]
image_path = os.path.join(output_dir, image_name)

try:
    # Скачиваем изображение
    response = requests.get(first_image_url)
    response.raise_for_status()  # Проверяем, что запрос успешен

    # Сохраняем изображение
    with open(image_path, 'wb') as file:
        file.write(response.content)

    print(f'Скачано: {image_name}')
except requests.exceptions.RequestException as e:
    print(f'Ошибка при скачивании {first_image_url}: {e}')
