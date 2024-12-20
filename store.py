import pygame
from config import *


def shop(player, player2):
    # creating the screen at 720x720 pixels
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height))

    store = pygame.image.load("ui/store.png")

    back = pygame.image.load("ui/back.png")
    back_w, back_h = back.get_width(), back.get_height()
    back_hover_size = (int(back_w * 1.2), int(back_h * 1.2))
    back_hover = pygame.transform.scale(back, back_hover_size)

    weapon = pygame.image.load("ui/weapon.png")
    weapon_w, weapon_h = weapon.get_width(), weapon.get_height()
    weapon_hover = pygame.image.load("ui/weapon_hover.png")

    skin = pygame.image.load("ui/skin.png")
    skin_w, skin_h = skin.get_width(), skin.get_height()
    skin_hover = pygame.image.load("ui/skin_hover.png")


    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    conversation_font = pygame.font.SysFont("Arial", 30)

    # setting my texts:
    back_text = corbelfont.render("back", True, white)
    # Initializing costs outside the loop
    upgrade_cost_1 = 250
    upgrade_cost_2 = 250
    skin_cost_1 = 1000
    skin_cost_2 = 1000

    # same old, same old while True loop
    while True:

        screen.blit(background, (0, 0))
        screen.blit(store, (115,95))

        # screen.blit(weapon, (130, 540))
        # screen.blit(weapon, (450, 540))

        #screen.blit(skin, (230, 540))
        #screen.blit(skin, (550, 540))

        # getting mouse position
        mouse = pygame.mouse.get_pos()

        # print(mouse[0], mouse[1]) 155,310

        if 10 <= mouse[0] <= 10 + back_w and 10 <= mouse[1] <= 10 + back_h:
            # scaling the original back button
            screen.blit(back_hover, (10 - (back_hover_size[0] - back_w) // 2,
                                     10 - (back_hover_size[1] - back_h) // 2))
        else:
            # if not hovering, then show the original back button
            screen.blit(back, (10, 10))

        if 130 <= mouse[0] <= 130 + weapon_w and 540 <= mouse[1] <= 540 + weapon_h:

            screen.blit(weapon_hover, (130 - (weapon_hover.get_width() - weapon_w) // 2,
                                     540 - (weapon_hover.get_height() - weapon_h) // 2))
        else:

            screen.blit(weapon, (130, 540))

        if 450 <= mouse[0] <= 450 + weapon_w and 540 <= mouse[1] <= 540 + weapon_h:
            screen.blit(weapon_hover, (450 - (weapon_hover.get_width() - weapon_w) // 2,
                                     540 - (weapon_hover.get_height() - weapon_h) // 2))
        else:
            # if not hovering, then show the original back button
            screen.blit(weapon, (450, 540))

        if 230 <= mouse[0] <= 230 + skin_w and 540 <= mouse[1] <= 540 + skin_h:

            screen.blit(skin_hover, (230 - (skin_hover.get_width() - skin_w) // 2,
                                       540 - (skin_hover.get_height() - skin_h) // 2))
        else:

            screen.blit(skin, (230, 540))

        if 550 <= mouse[0] <= 550 + skin_w and 540 <= mouse[1] <= 540 + skin_h:

            screen.blit(skin_hover, (550 - (skin_hover.get_width() - skin_w) // 2,
                                       540 - (skin_hover.get_height() - skin_h) // 2))
        else:

            screen.blit(skin, (550, 540))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 10 <= mouse[0] <= 100 and 10 <= mouse[1] <= 50:
                    save_file = "save_player_data.json"
                    save_file2 = "save_player_2_data.json"
                    player.save_player_data(save_file)
                    player2.save_player_data(save_file2)
                    return

                # Checking if the upgrade button for player 1 was clicked
                if 130 <= mouse[0] <= 130+weapon_w and 540 <= mouse[1] <= 540+weapon_h:
                    if player.coins >= upgrade_cost_1 and player.weapon_power <2:
                        player.coins -= upgrade_cost_1
                        player.weapon_power += 1
                        upgrade_cost_1 += 250  # Increase the cost for the next upgrade

                # Checking if the upgrade button for player 2 was clicked
                if 450 <= mouse[0] <= 450+weapon_w and 540 <= mouse[1] <= 540+weapon_h:
                    if player2.coins >= upgrade_cost_2 and player2.weapon_power < 2:
                        player2.coins -= upgrade_cost_2
                        player2.weapon_power += 1
                        upgrade_cost_2 += 250  # Increase the cost for the next upgrade

                # Checking if the shield button for player 1 was clicked
                if 230 <= mouse[0] <= 230+skin_w and 540 <= mouse[1] <= 540+skin_h:
                    if player.coins >= skin_cost_1 and player.skin < 2:
                        player.coins -= skin_cost_1
                        player.skin += 1
                        skin_cost_1 += 1000  # Increase the cost for the next shield

                # Checking if the shield button for player 2 was clicked
                if 550 <= mouse[0] <= 550+skin_w and 540 <= mouse[1] <= 540+skin_h:
                    if player2.coins >= skin_cost_2 and player2.skin < 2:
                        player2.coins -= skin_cost_2
                        player2.skin += 1
                        skin_cost_2 += 1000  # Increase the cost for the next shield


        # Displaying the player's current weapon power
        weapon_power_text = conversation_font.render(f"Weapon: {player.weapon_power}", True, white)
        screen.blit(weapon_power_text, (155,300))

        # Displaying the player's current shield
        skin_text = conversation_font.render(f"Skin: {player.skin}", True, white)
        screen.blit(skin_text, (155, 350))

        # Displaying the player's current coins
        coins_text = conversation_font.render(f"Coins: {player.coins}", True, white)
        screen.blit(coins_text, (155, 400))

        # Displaying player 2's current weapon power
        weapon_power_text_2 = conversation_font.render(f"Weapon: {player2.weapon_power}", True, white)
        screen.blit(weapon_power_text_2, (480,300))

        # Displaying player 2's current shield
        skin_text_2 = conversation_font.render(f"Skin: {player2.skin}", True, white)
        screen.blit(skin_text_2, (480, 350))

        # Displaying player 2's current coins
        coins_text_2 = conversation_font.render(f"Coins: {player2.coins}", True, white)
        screen.blit(coins_text_2, (480, 400))

        # finally, as always, updating our screen
        pygame.display.update()
