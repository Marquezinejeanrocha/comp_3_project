import pygame

pygame.mixer.init()

bullet_sound = pygame.mixer.Sound('sounds/singlebullet1.wav')
background_sound = pygame.mixer.Sound('sounds/audio_comp.wav')
interface_sound = pygame.mixer.Sound('sounds/interface_music.wav')


volume = 0.5
bullet_sound.set_volume(volume)
background_sound.set_volume(volume)
interface_sound.set_volume(volume)

def adjust_volume(change):
    """
    Adjust the volume of the sounds.
    Args:
        change (float): The amount to change the volume by. Positive values increase the volume,
                        while negative values decrease it.
    """
    global volume
    if volume + change > 1:
        volume = 1
    elif volume + change < 0:
        volume = 0
    else:
        volume += change
        
    bullet_sound.set_volume(volume)
    background_sound.set_volume(volume)
    interface_sound.set_volume(volume)
