import sounddevice as sd


def list_input_devices():
    devices = sd.query_devices()
    return [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]


def choose_device_by_name(name):
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if name.lower() in d['name'].lower() and d['max_input_channels'] > 0:
            return i
    return None


def choose_device_interactively():
    devices = sd.query_devices()
    input_devices = list_input_devices()
    for i in input_devices:
        print(f"{i}: {devices[i]['name']}")
    while True:
        try:
            index = int(input("🔧 Введите номер микрофона: "))
            if index in input_devices:
                return index
        except ValueError:
            pass
        print("⚠️ Неверный выбор. Попробуйте снова.")
        