import pygame
from config import *


def shop(player, player2):
    """
    Displays the shop interface where players can upgrade their weapons and skins.

    Args:
        player (Player): The first player object.
        player2 (Player): The second player object.

    The shop interface allows players to:
        - Upgrade their weapon power if they have enough coins.
        - Upgrade their skin if they have enough coins.
        - Return to the previous screen by clicking the back button.

    The function handles:
        - Displaying the shop UI elements such as background, buttons, and text.
        - Detecting mouse hover and click events on the buttons.
        - Updating player attributes based on their actions in the shop.
        - Saving player data and quitting the game when the window is closed.

    Note:
        This function runs an infinite loop to keep the shop interface active until the player decides to return.
    """
    # creating the screen and setting the background
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height))

    # loading the images
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
    conversation_font = pygame.font.SysFont("Arial", 30)
    small_font = pygame.font.SysFont("Arial", 15)


    # Initializing costs outside the loop
    upgrade_cost_1 = 250
    upgrade_cost_2 = 250
    skin_cost_1 = 1000
    skin_cost_2 = 1000

    while True:

        # setting the background and the store image
        screen.blit(background, (0, 0))
        screen.blit(store, (115,95))

        # getting mouse position
        mouse = pygame.mouse.get_pos()

        # checking if the mouse is hovering over the buttons
        #back button
        if 10 <= mouse[0] <= 10 + back_w and 10 <= mouse[1] <= 10 + back_h:
            # scaling the original back button
            screen.blit(back_hover, (10 - (back_hover_size[0] - back_w) // 2,
                                     10 - (back_hover_size[1] - back_h) // 2))
        else:
            screen.blit(back, (10, 10))

        # weapon upgrade buttons
        if 130 <= mouse[0] <= 130 + weapon_w and 540 <= mouse[1] <= 540 + weapon_h:
            screen.blit(weapon_hover, (130 - (weapon_hover.get_width() - weapon_w) // 2,
                                     540 - (weapon_hover.get_height() - weapon_h) // 2))
        else:
            screen.blit(weapon, (130, 540))

        if 450 <= mouse[0] <= 450 + weapon_w and 540 <= mouse[1] <= 540 + weapon_h:
            screen.blit(weapon_hover, (450 - (weapon_hover.get_width() - weapon_w) // 2,
                                     540 - (weapon_hover.get_height() - weapon_h) // 2))
        else:
            screen.blit(weapon, (450, 540))

        # skin upgrade buttons
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

        # handling events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                player.save_player_data("save_player_data.json")
                player2.save_player_data( "save_player_2_data.json")
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 10 <= mouse[0] <= 100 and 10 <= mouse[1] <= 50:
                    return

                # Checking if the upgrade button for player 1 was clicked
                if 130 <= mouse[0] <= 130+weapon_w and 540 <= mouse[1] <= 540+weapon_h:
       
                    if player.coins >= upgrade_cost_1 and player.weapon_power <2:
                        player.coins -= upgrade_cost_1
                        player.weapon_power += 1
                        upgrade_cost_1 += 250  # Increase the cost for the next upgrade

                # Same for player 2
                if 450 <= mouse[0] <= 450+weapon_w and 540 <= mouse[1] <= 540+weapon_h:
                    if player2.coins >= upgrade_cost_2 and player2.weapon_power < 2:
                        player2.coins -= upgrade_cost_2
                        player2.weapon_power += 1
                        upgrade_cost_2 += 250  # Increase the cost for the next upgrade

                # Checking if the skin button for player 1 was clicked
                if 230 <= mouse[0] <= 230+skin_w and 540 <= mouse[1] <= 540+skin_h:
                    if player.coins >= skin_cost_1 and player.skin < 2:
                        player.coins -= skin_cost_1
                        player.skin += 1
                        skin_cost_1 += 1000  # Increase the cost for the next skin

                # Same for player 2
                if 550 <= mouse[0] <= 550+skin_w and 540 <= mouse[1] <= 540+skin_h:
                    if player2.coins >= skin_cost_2 and player2.skin < 2:
                        player2.coins -= skin_cost_2
                        player2.skin += 1
                        skin_cost_2 += 1000  # Increase the cost for the next skin


        # Displaying the player's current weapon power
        weapon_power_text = conversation_font.render(f"Weapon: {player.weapon_power}", True, white)
        screen.blit(weapon_power_text, (155, 300))

        # Displaying the cost of the next upgrade for player 1
        if player.weapon_power < 2:
            upgrade_cost_text = small_font.render(f"Price: {upgrade_cost_1} $", True, white)
        else:
            upgrade_cost_text = small_font.render("Fully upgraded", True, white)
        screen.blit(upgrade_cost_text, (155, 340))

        # Displaying the player's current skin
        skin_text = conversation_font.render(f"Skin: {player.skin}", True, white)
        screen.blit(skin_text, (155, 370))

        # Displaying the cost of the next skin upgrade for player 1
        if player.skin < 2:
            skin_cost_text = small_font.render(f"Price: {skin_cost_1} $", True, white)
        else:
            skin_cost_text = small_font.render("Fully upgraded", True, white)
        screen.blit(skin_cost_text, (155, 415))

        # Displaying the player's current coins
        coins_text = conversation_font.render(f"Coins: {player.coins}", True, white)
        screen.blit(coins_text, (155, 440))

        # Displaying player 2's current weapon power
        weapon_power_text_2 = conversation_font.render(f"Weapon: {player2.weapon_power}", True, white)
        screen.blit(weapon_power_text_2, (480, 300))

        # Displaying the cost of the next upgrade for player 2
        if player2.weapon_power < 2:
            upgrade_cost_text_2 = small_font.render(f"Price: {upgrade_cost_2} $", True, white)
        else:
            upgrade_cost_text_2 = small_font.render("Fully upgraded", True, white)
        screen.blit(upgrade_cost_text_2, (480, 340))

        # Displaying player 2's current skin
        skin_text_2 = conversation_font.render(f"Skin: {player2.skin}", True, white)
        screen.blit(skin_text_2, (480, 370))

        # Displaying the cost of the next skin upgrade for player 2
        if player2.skin < 2:
            skin_cost_text_2 = small_font.render(f"Price: {skin_cost_2} $", True, white)
        else:
            skin_cost_text_2 = small_font.render("Fully upgraded", True, white)
        screen.blit(skin_cost_text_2, (480, 415))

        # Displaying player 2's current coins
        coins_text_2 = conversation_font.render(f"Coins: {player2.coins}", True, white)
        screen.blit(coins_text_2, (480, 440))

        # finally, as always, updating our screen
        pygame.display.update()
