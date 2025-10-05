import vosk
import sounddevice as sd
import queue
import json
from config import TRIGGER_PHRASES
from actions import execute_action


class VoiceRecognizer:
    def __init__(self, model_path, device_index, logger):
        self.model = vosk.Model(model_path)
        self.device_index = device_index
        self.q = queue.Queue()
        self.rec = vosk.KaldiRecognizer(self.model, 16000)
        self.logger = logger

    def _callback(self, indata, frames, time, status):
        if status:
            self.logger.warning(f"Аудио статус: {status}")
        self.q.put(bytes(indata))

    def listen(self):
        with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                               channels=1, device=self.device_index, callback=self._callback):
            self.logger.info("Начато прослушивание службы")
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").lower()
                    if text.strip():
                        self.logger.info(f"Распознано: {text}")
                        for phrase, action_name in TRIGGER_PHRASES.items():
                            if phrase in text:
                                self.logger.info(f"Сработала фраза: '{phrase}' → действие: {action_name}")
                                execute_action(action_name)
                                break
                else:
                    result = json.loads(self.rec.PartialResult())
                    text = result.get("text", "").lower()
                    if text.strip():
                        self.logger.info(f"Распознано Partial: {text}")
                  
