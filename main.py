from pynput.keyboard import Controller as KeyController
from pynput import keyboard
import time

keyCount = 0
keyAndInterval = []

paused = False
running = True
controller = KeyController()
listener = None


def bail():
    global running
    if listener is not None:
        listener.stop()
    running = False


def configure():
    global keyCount
    keyCount = int(input("How many distinct keys:"))
    for x in range(keyCount):
        key = input("Key to press:")
        if len(key) > 1:
            print("Error {} is not a key ".format(key))
            raise SystemExit
        interval = float(input("Interval millis :"))
        keyAndInterval.append((key, interval))
    keyAndInterval.sort(key=lambda a: a[1])

    log = "Pressing [key,interval]-> "
    for ki in keyAndInterval:
        print(ki)
        log += "[K={},I={}], ".format(ki[0], ki[1])
    print(log)
    print("F3 to pause/resume")


def press(key):
    controller.press(key)
    controller.release(key)


def run_loop():
    global listener

    def on_pause_release(pause_key):
        global paused
        if pause_key == keyboard.Key.f3:
            print("Resuming" if paused else "\nPausing")
            paused = not paused

    listener = keyboard.Listener(
        on_press=None,
        on_release=on_pause_release)
    listener.start()

    # TODO: optimally should be highest common divisor
    wait_between_loops = 10
    keys = []
    for k in keyAndInterval:
        keys.append({'key': k[0], 'delay': k[1], 'pressedAt': 0})

    while running:
        if not paused:
            now = time.time()*1000
            for k in keys:
                if k['pressedAt'] + k['delay'] <= now:
                    press(k['key'])
                    k['pressedAt'] = now
        try:
            time.sleep(wait_between_loops / 1000)
        except KeyboardInterrupt:
            bail()


if __name__ == "__main__":
    configure()
    run_loop()
