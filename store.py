import pygame
from config import *


def shop(player, player2):
    # creating the screen at 720x720 pixels
    screen = pygame.display.set_mode(resolution)

    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    conversation_font = pygame.font.SysFont("Arial", 30)

    # setting my texts:
    back_text = corbelfont.render("back", True, white)
    # Initializing costs outside the loop
    upgrade_cost_1 = 10
    upgrade_cost_2 = 10
    skin_cost_1 = 15
    skin_cost_2 = 15

    # same old, same old while True loop
    while True:
        # getting mouse position
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80:
                    save_file = "save_player_data.json"
                    save_file2 = "save_player_2_data.json"
                    player.save_player_data(save_file)
                    player2.save_player_data(save_file2)
                    return

                # Checking if the upgrade button for player 1 was clicked
                if 100 <= mouse[0] <= 340 and 500 <= mouse[1] <= 560:
                    if player.coins >= upgrade_cost_1:
                        player.coins -= upgrade_cost_1
                        player.weapon_power += 1
                        upgrade_cost_1 += 10  # Increase the cost for the next upgrade

                # Checking if the upgrade button for player 2 was clicked
                if 380 <= mouse[0] <= 620 and 500 <= mouse[1] <= 560:
                    if player2.coins >= upgrade_cost_2:
                        player2.coins -= upgrade_cost_2
                        player2.weapon_power += 1
                        upgrade_cost_2 += 10  # Increase the cost for the next upgrade

                # Checking if the shield button for player 1 was clicked
                if 100 <= mouse[0] <= 340 and 600 <= mouse[1] <= 660:
                    if player.coins >= skin_cost_1:
                        player.coins -= skin_cost_1
                        player.skin += 1
                        skin_cost_1 += 15  # Increase the cost for the next shield

                # Checking if the shield button for player 2 was clicked
                if 380 <= mouse[0] <= 620 and 600 <= mouse[1] <= 660:
                    if player2.coins >= skin_cost_2:
                        player2.coins -= skin_cost_2
                        player2.skin += 1
                        skin_cost_2 += 15  # Increase the cost for the next shield

        # display the screen:
        screen.fill(deep_black)

        # drawing the back button
        pygame.draw.rect(screen, dark_red, [20, 20, 140, 60])
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 20 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Drawing the upgrade button for player 1
        upgrade_text = corbelfont.render("Upgrade 1", True, white)
        pygame.draw.rect(screen, green, [50, 500, 300, 60])
        upgrade_rect = upgrade_text.get_rect(center=(50 + 300 // 2, 500 + 60 // 2))
        screen.blit(upgrade_text, upgrade_rect)

        # Drawing the upgrade button for player 2
        upgrade_text_2 = corbelfont.render("Upgrade 2", True, white)
        pygame.draw.rect(screen, green, [370, 500, 300, 60])
        upgrade_rect_2 = upgrade_text_2.get_rect(center=(370 + 300 // 2, 500 + 60 // 2))
        screen.blit(upgrade_text_2, upgrade_rect_2)

        # Drawing the shield button for player 1
        skin_text = corbelfont.render("skin 1", True, white)
        pygame.draw.rect(screen, blue, [50, 600, 300, 60])
        skin_rect = skin_text.get_rect(center=(50 + 300 // 2, 600 + 60 // 2))
        screen.blit(skin_text, skin_rect)

        # Drawing the shield button for player 2
        skin_text_2 = corbelfont.render("skin 2", True, white)
        pygame.draw.rect(screen, blue, [370, 600, 300, 60])
        skin_rect_2 = skin_text_2.get_rect(center=(370 + 300 // 2, 600 + 60 // 2))
        screen.blit(skin_text_2, skin_rect_2)

        # Displaying the player's current weapon power
        weapon_power_text = conversation_font.render(f"Player 1 Weapon Power: {player.weapon_power}", True, white)
        weapon_power_rect = weapon_power_text.get_rect(center=(720 // 2, 100))
        screen.blit(weapon_power_text, weapon_power_rect)

        # Displaying player 2's current weapon power
        weapon_power_text_2 = conversation_font.render(f"Player 2 Weapon Power: {player2.weapon_power}", True, white)
        weapon_power_rect_2 = weapon_power_text_2.get_rect(center=(720 // 2, 150))
        screen.blit(weapon_power_text_2, weapon_power_rect_2)

        # Displaying the player's current shield
        skin_text = conversation_font.render(f"Player 1 skin: {player.skin}", True, white)
        skin_rect = skin_text.get_rect(center=(720 // 2, 200))
        screen.blit(skin_text, skin_rect)

        # Displaying player 2's current shield
        skin_text_2 = conversation_font.render(f"Player 2 skin: {player2.skin}", True, white)
        skin_rect_2 = skin_text_2.get_rect(center=(720 // 2, 250))
        screen.blit(skin_text_2, skin_rect_2)

        # Displaying the player's current coins
        coins_text = conversation_font.render(f"Player 1 Coins: {player.coins}", True, white)
        coins_rect = coins_text.get_rect(center=(720 // 2, 300))
        screen.blit(coins_text, coins_rect)

        # Displaying player 2's current coins
        coins_text_2 = conversation_font.render(f"Player 2 Coins: {player2.coins}", True, white)
        coins_rect_2 = coins_text_2.get_rect(center=(720 // 2, 350))
        screen.blit(coins_text_2, coins_rect_2)

        # finally, as always, updating our screen
        pygame.display.update()
