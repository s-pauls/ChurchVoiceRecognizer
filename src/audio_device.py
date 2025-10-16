import sounddevice as sd


def list_input_devices():
    devices = sd.query_devices()
    return {i: d['name'] for i, d in enumerate(devices) if d['max_input_channels'] > 0}


def choose_device_by_name(name):
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if name.lower() in d['name'].lower() and d['max_input_channels'] > 0:
            return i
    return None