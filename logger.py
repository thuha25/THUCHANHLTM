callbacks = []


def register_callback(callback):
    callbacks.append(callback)


def log(message):
    print(message)
    for callback in callbacks:
        callback(message)
