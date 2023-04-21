from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyController
from pynput import keyboard, mouse
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
import sys
import os
import time

asciiart = """

                _        _  __          
     /\        | |      | |/ /          
    /  \  _   _| |_ ___ | ' / ___ _   _ 
   / /\ \| | | | __/ _ \|  < / _ \ | | |
  / ____ \ |_| | || (_) | . \  __/ |_| |
 /_/    \_\__,_|\__\___/|_|\_\___|\__, |
                                   __/ |
                                  |___/ 
                            
Fork of : git@github.com:kaleidosc/AutoKey.git                             
"""

key = '1'
intervalMillis = '1000'
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
    global key
    global intervalMillis
    key = input("Key to press :")
    intervalMillis = float(input("Interval millis :"))
    print('Pressing "{}" every {} millis.'.format(key, intervalMillis))
    print("F3 to pause/resume")


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

    while running:
        if not paused:
            controller.press(key)
            controller.release(key)
        try:
            time.sleep(intervalMillis/1000)
        except KeyboardInterrupt:
            bail()


if __name__ == "__main__":
    configure()
    run_loop()
