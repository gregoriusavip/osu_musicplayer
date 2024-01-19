import pygame
from error_handler import error_handler
from collections import deque
import logging
import os
import settings

pygame.init()
pygame.mixer.init()
MAX_SIZE = 100
MUSIC_END = pygame.USEREVENT + 1       # assign the first slot of pygame's EVENT ID
pygame.mixer.music.set_endevent(MUSIC_END)

_song_list = deque()
_history_song_list = deque()

def loader(file: str):
    """
    Function to load a song to the queue. 
    This will reset the queue, load, and play user's selected song
    """
    global _song_list, _history_song_list
    try:
        pygame.mixer.music.load(os.path.join(settings.OSU_FOLDER, file))
        pygame.mixer.music.play()
        _song_list = deque([file, r"950550 VALLEYSTONE feat KanataN - Natsuirozaka\audio.mp3", r"1180927 PassCode - Ray\audio.mp3"])   # TODO: generate the next songs
        _history_song_list = deque() # empty the past queue
    except pygame.error as e:
        logging.error("Error detected")
        error_handler(e, "Loading file")

"""
def queue_song(file: str):
    BASE_SONG_FOLDER = os.path.join(settings.OSU_FOLDER, "songs")
    song_list.push_back(os.path.join(BASE_SONG_FOLDER, file))
"""

def pause():
    """
    Pause currently loaded music.
    """
    pygame.mixer.music.pause()

def unpause():
    """
    Unpause the currently paused music
    """
    pygame.mixer.music.unpause()

def play_next():
    """
    Play the next song in the queue.
    """
    global _song_list, _history_song_list
    pygame.mixer.music.unload()
    if _song_list:
        _history_song_list.append(_song_list.popleft())
        pygame.mixer.music.load(os.path.join(settings.OSU_FOLDER, _song_list[0]))
        pygame.mixer.music.play()

def play_previous():
    """
    Play the previous song stored in the history queue.
    """
    global _song_list, _history_song_list
    if _history_song_list:
        pygame.mixer.music.unload()
        _song_list.appendleft(_history_song_list.popleft())
        pygame.mixer.music.load(os.path.join(settings.OSU_FOLDER, _song_list[0]))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.play()

display = pygame.display.set_mode((300, 300))
def test():
    
    file = r"1692335 Feryquitous feat Aitsuki Nakuru - Kairikou\audio.mp3"
    loader(file)
    loop = False
        
    while True:
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                if loop:
                    pygame.mixer.music.play()
                else:
                    play_next()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_u:
                    unpause()
                if event.key == pygame.K_l:
                    loop = not loop
                if event.key == pygame.K_f:
                    play_next()
                if event.key == pygame.K_b:
                    play_previous()