import pygame

from config import dark_red, deep_black, resolution, white
from game import dark_red, deep_black, pygame, resolution, white
import sounds

  


def options():


    # creating the screen at 720x720 pixels
    screen = pygame.display.set_mode(resolution)

    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    conversation_font = pygame.font.SysFont("Arial", 30)

    # setting my texts:
    back_text = corbelfont.render("back", True, white)
    volume_text = corbelfont.render("Volume", True, white)
    volume_up_text = corbelfont.render("+", True, white)
    volume_down_text = corbelfont.render("-", True, white)



    # same old, same old while True loop
    while True:
        # getting mouse position
        volume = sounds.volume
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    return
                # checking if the volume up button was clicked
                if 350 <= mouse[0] <= 390 and 300 <= mouse[1] <= 340:
                        sounds.adjust_volume(0.1)

                # checking if the volume down button was clicked
                if 250 <= mouse[0] <= 290 and 300 <= mouse[1] <= 340:
                        sounds.adjust_volume(-0.1)

            # display the screen:
            screen.fill(deep_black)

            # drawing the back button
            pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
            back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
            screen.blit(back_text, back_rect)

            # drawing the volume controls
            screen.blit(volume_text, (200, 200))
            pygame.draw.rect(screen, dark_red, [250, 300, 40, 40])
            pygame.draw.rect(screen, dark_red, [350, 300, 40, 40])
            volume_down_rect = volume_down_text.get_rect(center=(250 + 40 // 2, 300 + 40 // 2))
            volume_up_rect = volume_up_text.get_rect(center=(350 + 40 // 2, 300 + 40 // 2))
            screen.blit(volume_down_text, volume_down_rect)
            screen.blit(volume_up_text, volume_up_rect)

            # displaying the current volume level
            current_volume_text = corbelfont.render(str(int(volume*100)), True, white)
            screen.blit(current_volume_text, (300, 300))

            # finally, as always, updating our screen
            pygame.display.update()


         

            # finally, as always, updating our screen
            pygame.display.update()
            