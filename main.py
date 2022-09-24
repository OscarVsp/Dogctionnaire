# -*- coding: utf-8 -*-
from json import load
from signal import pause
from typing import List

from gpiozero import Button
from pygame.mixer import init
from pygame.mixer import music
from pygame.mixer import Sound

pins: List[int] = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40]
path: str = "./sounds/"


def dogctionnaire():
    init()
    sounds: List[Sound] = []

    # Load data from data.json
    try:
        print('Loading data from .json...')
        with open("data.json", "r") as fp:
            data: dict = load(fp)
            music.set_volume(data.get("volume_global", 1.0))
            for sound_data in data.get("sounds", []):
                new_sound = Sound(path + sound_data.get("filename", "not_found.mp3"))
                new_sound.set_volume(sound_data.get("volume", 1.0))
                sounds.append(new_sound)
                print(f"Sound {sound_data.get('filename','not_found.mp3')} load at position {len(sounds)}")
    except Exception as ex:
        print(f'Error loading data from .json: {ex}')

    # Add dummy sounds for remaining button
    for _ in range(len(pins) - len(sounds)):
        dummy_sound = Sound(path + "not_found.mp3")
        sounds.append(dummy_sound)

    # Map pins to sounds with buttons
    print(f"Mapping buttons")
    for i, pin_num in enumerate(pins):
        new_button = Button(pin_num)
        new_button.when_activated = sounds[i].play

    print("Ready !")
    pause()


if __name__ == "__main__":
    print('Starting...')
    dogctionnaire()
