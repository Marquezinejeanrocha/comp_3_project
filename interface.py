import pygame
from utils import *  
from config import *  
from game import *
from utils import *
from store import shop
from player import Player
from sounds import interface_sound

#creatting the player for the game
controls_player1 = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
}

controls_player2 = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}
player = Player(cute_purple, (110,106), controls_player1)
player2 = Player(greenish, (612,601), controls_player2)

def interface():
    """
    Initializes the game interface and handles the main menu interactions.
    This function performs the following tasks:
    - Loads player data from JSON files or creates new save files if they do not exist.
    - Initializes the Pygame library and sets up the game screen.
    - Loads and scales various UI elements such as background, buttons, and game title.
    - Displays the main menu with hover effects for buttons.
    - Handles user interactions with the main menu, including button clicks for starting the game, opening the shop, viewing credits, options, and rules, and quitting the game.
    - Saves player data upon quitting the game.
    Raises:
        FileNotFoundError: If the save files for player data do not exist and need to be created.
    """


    # Define save file names for player data
    save_file = "save_player_data.json"
    save_file2 = "save_player_2_data.json"

    # Attempt to load player data from save files, create new save files if they do not exist
    try:
        with open(save_file, 'r'):
            player.load_player_data(save_file)
    except FileNotFoundError:
        player.save_player_data(save_file)

    try:
        with open(save_file2, 'r'):
            player2.load_player_data(save_file2)
    except FileNotFoundError:
        player2.save_player_data(save_file2)

    # Initialize Pygame
    pygame.init()

    # Play the interface sound
    interface_sound.play()

    # Create the game screen with the specified resolution
    screen = pygame.display.set_mode(resolution)

    # Load and scale the background image to fill the entire screen
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height))

    # Load the game title image
    game = pygame.image.load("ui/CHEST BUSTER.png")

    # Load and scale the buttons and their hover effects
    play = pygame.image.load("ui/play.png")
    play_w, play_h = play.get_width(), play.get_height()
    play_hover_size = (play_w * 1.2, play_h * 1.2)
    play_hover = pygame.transform.scale(play, play_hover_size)

    shops = pygame.image.load("ui/shop.png")
    shop_w, shop_h = shops.get_width(), shops.get_height()
    shop_hover_size = (int(shop_w * 1.2), int(shop_h * 1.2))
    shop_hover = pygame.transform.scale(shops, shop_hover_size)

    credit = pygame.image.load("ui/credit.png")
    credit_w, credit_h = credit.get_width(), credit.get_height()
    credit_hover_size = (int(credit_w * 1.2), int(credit_h * 1.2))
    credit_hover = pygame.transform.scale(credit, credit_hover_size)

    option = pygame.image.load("ui/option.png")
    option_w, option_h = option.get_width(), option.get_height()
    option_hover_size = (int(option_w * 1.2), int(option_h * 1.2))
    option_hover = pygame.transform.scale(option, option_hover_size)

    rules = pygame.image.load("ui/rule_btn.png")
    rules_w, rules_h = rules.get_width(), rules.get_height()
    rules_hover_size = (int(rules_w * 1.2), int(rules_h * 1.2))
    rules_hover = pygame.transform.scale(rules, rules_hover_size)

    back = pygame.image.load("ui/back.png")
    back_w, back_h = back.get_width(), back.get_height()
    back_hover_size = (int(back_w * 1.2), int(back_h * 1.2))
    back_hover = pygame.transform.scale(back, back_hover_size)

    quit = pygame.image.load("ui/quit.png")
    quit_w, quit_h = quit.get_width(), quit.get_height()
    quit_hover_size = (int(quit_w * 1.2), int(quit_h * 1.2))
    quit_hover = pygame.transform.scale(quit, quit_hover_size)

    # Ensure the game over video is not shown initially
    game_over.video_shown = False

    while True:
        # Fill the screen with the background image
        screen.blit(background, (0, 0))
        screen.blit(game, (160, 120))
        mouse = pygame.mouse.get_pos()

        # Buttons with hover effect
        if 280 <= mouse[0] <= 280 + play_w and 275 <= mouse[1] <= 275 + play_h:
            screen.blit(play_hover, (280 - (play_hover_size[0] - play_w) // 2,
                         275 - (play_hover_size[1] - play_h) // 2))
        else:
            screen.blit(play, (280, 275))
        # Shop button
        if 105 <= mouse[0] <= 105 + shop_w and 420 <= mouse[1] <= 420 + shop_h:
            screen.blit(shop_hover, (105 - (shop_hover_size[0] - shop_w) // 2,
                         420 - (shop_hover_size[1] - shop_h) // 2))
        else:
            screen.blit(shops, (105, 420))

        # Credits button
        if 105 <= mouse[0] <= 105 + credit_w and 520 <= mouse[1] <= 520 + credit_h:
            screen.blit(credit_hover, (105 - (credit_hover_size[0] - credit_w) // 2,
                           520 - (credit_hover_size[1] - credit_h) // 2))
        else:
            screen.blit(credit, (105, 520))

        # Options button
        if 505 <= mouse[0] <= 505 + option_w and 420 <= mouse[1] <= 420 + option_h:
            screen.blit(option_hover, (505 - (option_hover_size[0] - option_w) // 2,
                           420 - (option_hover_size[1] - option_h) // 2))
        else:
            screen.blit(option, (505, 420))

        # Rules button
        if 505 <= mouse[0] <= 505 + rules_w and 520 <= mouse[1] <= 520 + rules_h:
            screen.blit(rules_hover, (505 - (rules_hover_size[0] - rules_w) // 2,
                          520 - (rules_hover_size[1] - rules_h) // 2))
        else:
            screen.blit(rules, (505, 520))

        # Quit button
        if 280 <= mouse[0] <= 280 + quit_w and 600 <= mouse[1] <= 600 + quit_h:
            screen.blit(quit_hover, (280 - (quit_hover_size[0] - quit_w) // 2,
                         600 - (quit_hover_size[1] - quit_h) // 2))
        else:
            screen.blit(quit, (280, 600))

        # Event loop to handle user input
        for ev in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            '''if ev.type == pygame.MOUSEBUTTONDOWN:
                print(mouse[0], mouse[1])'''
            # Exit button
            if ev.type == pygame.QUIT:
                player.save_player_data("save_player_data.json")
                player2.save_player_data( "save_player_2_data.json")
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Quit button
                if 280 <= mouse[0] <= 280 + quit_w and 600 <= mouse[1] <= 600 + quit_h:
                    player.save_player_data("save_player_data.json")
                    player2.save_player_data( "save_player_2_data.json")
                    pygame.quit()

                # Credits button
                if 105 <= mouse[0] <= 105 + credit_w and 520 <= mouse[1] <= 520 + credit_h:
                    credits_()

                # Play button
                if 280 <= mouse[0] <= 280 + play_w and 275 <= mouse[1] <= 275 + play_h:
                    interface_sound.stop()
                    game_loop(player, player2)

                # Shop button
                if 105 <= mouse[0] <= 105 + shop_w and 420 <= mouse[1] <= 420 + shop_h:
                    shop(player, player2)

                # Options button
                if 505 <= mouse[0] <= 505 + option_w and 420 <= mouse[1] <= 420 + option_h:
                    options(player, player2)

                # Rules button
                if 505 <= mouse[0] <= 505 + rules_w and 520 <= mouse[1] <= 520 + rules_h:
                    rules_()

        # update the display so that the loop changes will appear
        pygame.display.update()

def credits_():
    """
    Display the credits screen with the names of the group.

    Handles:
    - Mouse hover and click on the back button.
    - Quitting the game and saving player data.
    """
    # setting up the background
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height))

    # loading the credits image
    back = pygame.image.load("ui/back.png")
    credit = pygame.image.load("ui/credit_img.png")

    # Initial back button size
    back_width, back_height = back.get_width(), back.get_height()
    back_hover_size = (int(back_width * 1.3), int(back_height * 1.3))

    # screen setup:
    screen = pygame.display.set_mode(resolution)


    cont = True
    while cont:
        screen.blit(background, (0, 0))  
        screen.blit(credit, (100, 100))  # putting rules img on the screen

        # getting the position of the users mouse
        mouse = pygame.mouse.get_pos()

        # looking for mouse hover on top of back button
        if 10 <= mouse[0] <= 10 + back_width and 10 <= mouse[1] <= 10 + back_height:
            # scaling the original back button
            back_hover = pygame.transform.scale(back, back_hover_size)
            screen.blit(back_hover, (10 - (back_hover_size[0] - back_width) // 2,
                                     10 - (back_hover_size[1] - back_height) // 2))
        else:
            # if not hovering, then show the original back button
            screen.blit(back, (10, 10))

        for ev in pygame.event.get():

            # Exit button
            if ev.type == pygame.QUIT:
                player.save_player_data("save_player_data.json")
                player2.save_player_data( "save_player_2_data.json")
                pygame.quit()

            # Back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= mouse[0] <= 100 and 10 <= mouse[1] <= 50:
                    cont = False

        # updating the display
        pygame.display.update()


def rules_():
    """
    Displays the rules screen with the rules of the game.
    Handles user input and updates the display accordingly.
    """

    # setting up the background
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height))

    # loading the rules image
    back = pygame.image.load("ui/back.png")
    rules = pygame.image.load("ui/rules.png")

    # Initial back button size
    back_width, back_height = back.get_width(), back.get_height()
    back_hover_size = (int(back_width * 1.3), int(back_height * 1.3))

    # screen setup:
    screen = pygame.display.set_mode(resolution)

    cont = True
    while cont:
        screen.blit(background, (0, 0))
        screen.blit(rules,(60,70)) # putting rules image on the screen

        # getting the position of the users mouse
        mouse = pygame.mouse.get_pos()

        # looking for mouse hover on top of back button
        if 10 <= mouse[0] <= 10 + back_width and 10 <= mouse[1] <= 10 + back_height:
            # scaling the original back button
            back_hover = pygame.transform.scale(back, back_hover_size)
            screen.blit(back_hover, (10 - (back_hover_size[0] - back_width) // 2,
                                     10 - (back_hover_size[1] - back_height) // 2))
        else:
            # if not hovering, then show the original back button
            screen.blit(back, (10, 10))

        for ev in pygame.event.get():

            # Exit button
            if ev.type == pygame.QUIT:
                player.save_player_data("save_player_data.json")
                player2.save_player_data( "save_player_2_data.json")
                pygame.quit()

            # checking if the user clicked the back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= mouse[0] <= 100 and 10 <= mouse[1] <= 50:
                    cont = False

        # updating the display
        pygame.display.update()


