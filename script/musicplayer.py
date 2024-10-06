from pygame import mixer
from os import listdir
from time import sleep
from threading import Thread
from settings import window_and_objects as winaobj

mixer.init()

channel = mixer.Channel(1)

def volume_off():
    channel.set_volume(0)
def volume_on():
    channel.set_volume(100)

def player():
    sleep(winaobj.MUSIC_START_IS)
    try:
        for a in range(100):
            for i in listdir('music'):
                music = mixer.Sound(f'music/{i}')
                channel.play(music, loops=winaobj.MUSIC_LOOPS)
                print(f'\nPlaying: {i[:-4]} \nDuration: {int(music.get_length())} seconds \nRepeat - {winaobj.MUSIC_LOOPS}')
                sleep(music.get_length()*winaobj.MUSIC_LOOPS)
            if a == 100:
                return 0
    except:
        return 0

player_enable = Thread(target=player)
player_enable.start()