import vosk
import sounddevice as sd
import queue
import json

from src.liturgy_fsm import LiturgyFSM


class VoiceRecognizer:
    def __init__(self, model_path, device_index, logger, trigger_phrases=None):
        self.model = vosk.Model(model_path)
        self.device_index = device_index
        self.q = queue.Queue()
        self.rec = vosk.KaldiRecognizer(self.model, 16000)
        self.logger = logger
        self.processor = LiturgyFSM(logger)

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
                        self.processor.process_phrase(text)
                else:
                    result = json.loads(self.rec.PartialResult())
                    text = result.get("text", "").lower()
                    if text.strip():
                        self.logger.info(f"Распознано Partial: {text}")
                        # todo? self.processor.process_phrase(text)
                  
