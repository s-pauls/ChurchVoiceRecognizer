import time

class LiturgyFSM:
    def __init__(self, logger):
        self.state = "START"
        self.otche_count = 0
        self.block_start_time = None
        self.block_timeout = 600  # 10 минут в секундах
        self.logger=logger

    def action_1(self):
        print("✅ Действие 1: Обработка 'Отче наш' + 'имя Твое'")

    def action_2(self):
        print("✅ Действие 2: Обработка 'Господи помилуй' после молитвы")

    def start_block_timer(self):
        self.block_start_time = time.time()

    def check_timeout(self):
        if self.block_start_time and (time.time() - self.block_start_time > self.block_timeout):
            print("⏱️ Таймер истёк. Переход к следующему блоку.")
            if self.state.startswith("THIRD_HOUR"):
                self.state = "THIRD_HOUR_END"
                print("Переход в состояние: THIRD_HOUR_END")
            elif self.state.startswith("SIXTH_HOUR"):
                self.state = "SIXTH_HOUR_END"
                print("Переход в состояние: SIXTH_HOUR_END")
            self.block_start_time = None

    def process_phrase(self, phrase):
        phrase = phrase.lower()
        self.check_timeout()

        if self.state == "START":
            if "царю небесный" in phrase:
                self.state = "THIRD_HOUR_START"
                self.otche_count = 0
                self.start_block_timer()
                print("▶️ Переход в состояние: THIRD_HOUR_START")

        elif self.state == "THIRD_HOUR_START":
            if "отче наш" in phrase and "имя твое" in phrase:
                self.otche_count += 1
                self.action_1()
                if self.otche_count == 1:
                    self.state = "THIRD_HOUR_OTCHE_1"
                elif self.otche_count == 2:
                    self.state = "THIRD_HOUR_OTCHE_2"
                print(f"▶️ Переход в состояние: {self.state}")

        elif self.state == "THIRD_HOUR_OTCHE_1":
            if "господи помилуй" in phrase:
                self.action_2()

        elif self.state == "THIRD_HOUR_OTCHE_2":
            if "господи помилуй" in phrase:
                self.action_2()
                self.state = "THIRD_HOUR_END"
                self.block_start_time = None
                print("▶️ Переход в состояние: THIRD_HOUR_END")

        elif self.state == "THIRD_HOUR_END":
            if "царю небесный" in phrase:
                self.state = "SIXTH_HOUR_START"
                self.start_block_timer()
                print("▶️ Переход в состояние: SIXTH_HOUR_START")

        elif self.state == "SIXTH_HOUR_START":
            if "отче наш" in phrase and "имя твое" in phrase:
                self.action_1()
                self.state = "SIXTH_HOUR_OTCHE"
                print("▶️ Переход в состояние: SIXTH_HOUR_OTCHE")

        elif self.state == "SIXTH_HOUR_OTCHE":
            if "господи помилуй" in phrase:
                self.action_2()
                self.state = "SIXTH_HOUR_END"
                self.block_start_time = None
                print("▶️ Переход в состояние: SIXTH_HOUR_END")

    def reset(self):
        self.state = "START"
        self.otche_count = 0
        self.block_start_time = None
        print("🔄 FSM сброшен в начальное состояние")

# Пример использования:
fsm = LiturgyFSM()

# Симуляция распознанных фраз с задержками
phrases = [
    ("Царю небесный", 0),
    ("Святый Боже", 2),
    ("Святый Крепкий", 2),
    ("Отче наш, да святится имя Твое", 3),
    ("Господи помилуй", 2),
    ("Отче наш, да святится имя Твое", 3),
    ("Господи помилуй", 2),
    ("Царю небесный", 5),
    ("Святый Боже", 2),
    ("Отче наш, да святится имя Твое", 3),
    ("Господи помилуй", 2)
]

for phrase, delay in phrases:
    time.sleep(delay)
    fsm.process_phrase(phrase)