import pygame

from config import *
from game import dark_red, deep_black, pygame, resolution, white
import sounds
import player


def options(player, player2):
    # creating the screen at 720x720 pixels
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height))


    reset = pygame.image.load("ui/reset.png")
    reset_width, reset_height = reset.get_width(), reset.get_height()
    reset_hover_size = (int(reset_width * 1.3), int(reset_height * 1.3))
    reset_hover = pygame.transform.scale(reset, reset_hover_size)

    # Initial back button size
    back = pygame.image.load("ui/back.png")
    back_width, back_height = back.get_width(), back.get_height()
    back_hover_size = (int(back_width * 1.3), int(back_height * 1.3))
    back_hover = pygame.transform.scale(back, back_hover_size)
    # screen setup:
    screen = pygame.display.set_mode(resolution)

    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    conversation_font = pygame.font.SysFont("Arial", 30)

    # setting my texts:
    volume_text = corbelfont.render("Volume", True, white)
    volume_up_text = corbelfont.render("+", True, white)
    volume_down_text = corbelfont.render("-", True, white)

    # same old, same old while True loop
    while True:

        screen.blit(background, (0, 0))  # 0,0 will fill the entire screen
        # getting mouse position
        volume = sounds.volume
        mouse = pygame.mouse.get_pos()

        if 10 <= mouse[0] <= 10 + back_width and 10 <= mouse[1] <= 10 + back_height:
            # scaling the original back button
            back_hover = pygame.transform.scale(back, back_hover_size)
            screen.blit(back_hover, (10 - (back_hover_size[0] - back_width) // 2,
                                     10 - (back_hover_size[1] - back_height) // 2))
        else:
            # if not hovering, then show the original back button
            screen.blit(back, (10, 10))

        if 250 <= mouse[0] <= 250 + reset_width and 450 <= mouse[1] <= 450 + reset_height:
            # scaling the original back button
            screen.blit(reset_hover, (250 - (reset_hover_size[0] - reset_width) // 2,
                                     450 - (reset_hover_size[1] - reset_height) // 2))
        else:
            # if not hovering, then show the original back button
            screen.blit(reset, (250, 450))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                player.save_player_data("save_player_data.json")
                player2.save_player_data( "save_player_2_data.json")
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 10 <= mouse[0] <= 100 and 10 <= mouse[1] <= 50:
                    return
                # checking if the volume up button was clicked
                if 250 <= mouse[0] <= 290 and 300 <= mouse[1] <= 340:
                    sounds.adjust_volume(-0.1)
                # checking if the volume down button was clicked
                if 450 <= mouse[0] <= 490 and 300 <= mouse[1] <= 340:
                    sounds.adjust_volume(0.1)
                # checking if the reset player 1 button was clicked
                if 250 <= mouse[0] <= 250+reset_width and 450 <= mouse[1] <= 450+reset_height:
                    player.reset_player()
                    player2.reset_player()



            # drawing the volume controls
            screen.blit(volume_text, (285, 200))
            pygame.draw.rect(screen, dark_red, [250, 300, 40, 40])
            pygame.draw.rect(screen, dark_red, [450, 300, 40, 40])
            volume_down_rect = volume_down_text.get_rect(center=(250 + 40 // 2, 300 + 40 // 2))
            volume_up_rect = volume_up_text.get_rect(center=(450 + 40 // 2, 300 + 40 // 2))
            screen.blit(volume_down_text, volume_down_rect)
            screen.blit(volume_up_text, volume_up_rect)


            # displaying the current volume level
            current_volume_text = corbelfont.render(str(int(volume * 100)), True, white)
            screen.blit(current_volume_text, (350, 300))

            # finally, as always, updating our screen
            pygame.display.update()
