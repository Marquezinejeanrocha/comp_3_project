import pygame

pygame.mixer.init()

bullet_sound = pygame.mixer.Sound('sounds/singlebullet1.wav')
background_sound = pygame.mixer.Sound('sounds/audio_comp.wav')


volume = 0.5
bullet_sound.set_volume(volume)
background_sound.set_volume(volume)
def adjust_volume(change):
    global volume
    if volume + change > 1:
        volume = 1
    elif volume + change < 0:
        volume = 0
    else:
        volume += change
    bullet_sound.set_volume(volume)
    background_sound.set_volume(volume)
