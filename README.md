# 🎙️ Voice Trigger

Локальная система распознавания речи для служб на старославянском языке. Реагирует на ключевые фразы и выполняет действия.

## 🚀 Возможности

- Распознаёт фразы «отче наш» и «двери двери»
- Работает полностью локально (без интернета)
- Поддерживает выбор микрофона вручную
- Логирует все события в `voice_trigger.log`

## 📦 Установка

```bash
git clone https://github.com/yourusername/voice_trigger.git
cd src
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

📥 Модель Vosk
Скачай русскую модель отсюда: https://alphacephei.com/vosk/models
Распакуй в папку [models](/models)

🏁 Запуск
```bash
source venv/bin/activate  # или venv\Scripts\activate на Windows
python src/main.py
```

⚙️ Настройки
- Меньший blocksize → данные поступают в callback чаще → быстрее передаются в vosk. Это даст ~0.25 секунды аудио на блок (при samplerate=16000)


