import pygame
from config import *
from game import dark_red, resolution, white
import sounds


def options(player, player2):
    """
    Displays the options menu for the game, allowing the user to adjust settings such as volume and reset player data.

    Args:
        player (Player): The first player.
        player2 (Player): The second player.

    The function creates a Pygame window with various interactive elements:
        - A reset button to reset player data.
        - A back button to return to the previous menu.
        - Volume control buttons to increase or decrease the game volume.

    The function enters a loop where it continuously checks for user interactions and perform actions accordingly:
        - Hover effects for the reset and back buttons.
        - Adjusting the volume when the volume buttons are clicked.
        - Resetting player data when the reset button is clicked.
        - Saving player data and quitting the game when the window is closed.

    The function updates the display with the current volume level and other UI elements, and it exits when the back button is clicked.
    """
    # creating the screen
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height))

    # loading the images
    reset = pygame.image.load("ui/reset.png")
    reset_width, reset_height = reset.get_width(), reset.get_height()
    reset_hover_size = (int(reset_width * 1.3), int(reset_height * 1.3))
    reset_hover = pygame.transform.scale(reset, reset_hover_size)

    back = pygame.image.load("ui/back.png")
    back_width, back_height = back.get_width(), back.get_height()
    back_hover_size = (int(back_width * 1.3), int(back_height * 1.3))
    back_hover = pygame.transform.scale(back, back_hover_size)


    # screen setup:
    screen = pygame.display.set_mode(resolution)

    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)

    # setting my texts:
    volume_text = corbelfont.render("Volume", True, white)
    volume_up_text = corbelfont.render("+", True, white)
    volume_down_text = corbelfont.render("-", True, white)

    while True:
        # setting the background
        screen.blit(background, (0, 0)) 
        # getting the current volume level
        volume = sounds.volume
        # getting the mouse position
        mouse = pygame.mouse.get_pos()

        # checking if the buttons are being hovered over
        #back button
        if 10 <= mouse[0] <= 10 + back_width and 10 <= mouse[1] <= 10 + back_height:
            back_hover = pygame.transform.scale(back, back_hover_size)
            screen.blit(back_hover, (10 - (back_hover_size[0] - back_width) // 2,
                                     10 - (back_hover_size[1] - back_height) // 2))
        else:
            screen.blit(back, (10, 10))

        # volume up button
        if 250 <= mouse[0] <= 250 + reset_width and 450 <= mouse[1] <= 450 + reset_height:
            screen.blit(reset_hover, (250 - (reset_hover_size[0] - reset_width) // 2,
                                     450 - (reset_hover_size[1] - reset_height) // 2))
        else:
            screen.blit(reset, (250, 450))

        # checking for events
        for ev in pygame.event.get():
            # checking if the window was closed
            if ev.type == pygame.QUIT:
                player.save_player_data("save_player_data.json")
                player2.save_player_data( "save_player_2_data.json")
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Back button
                if 10 <= mouse[0] <= 100 and 10 <= mouse[1] <= 50:
                    return
                # Volume up button
                if 250 <= mouse[0] <= 290 and 300 <= mouse[1] <= 340:
                    sounds.adjust_volume(-0.1)
                # Volume down button
                if 450 <= mouse[0] <= 490 and 300 <= mouse[1] <= 340:
                    sounds.adjust_volume(0.1)
                # Reset player button
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
