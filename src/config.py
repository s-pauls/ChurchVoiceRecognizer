import os

# Получаем путь к корневой папке проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_TO_MODEL = os.path.join(PROJECT_ROOT, "models", "vosk-model-small-ru-0.22")
