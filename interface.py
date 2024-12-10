import pygame
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
from game import *
from utils import under_construction
from store import shop

def interface(): 
    # initiating pygame
    pygame.init() # calling pygame
    # creating the screen at the set resolution
    # show the user something
    screen = pygame.display.set_mode(resolution)
    #by default, I started the player in the main area
    players = initiate_players()
    player = players[0]
    player2 = players[1]

    # filling the screen
    # setting up the background
    background = pygame.image.load("ui/background.png")
    # para que o background ocupe toda a tela
    background = pygame.transform.scale(background, (width, height))
    game = pygame.image.load("ui/CHEST BUSTER.png")

    play = pygame.image.load("ui/play.png")
    play_w, play_h = play.get_width(), play.get_height()
    play_hover_size = (play_w * 1.2, play_h*1.2)
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
    while True:

        # 0,0 will fill the entire screen
        screen.blit(background, (0, 0))
        screen.blit(game, (160,120))
        mouse = pygame.mouse.get_pos()

        if 280 <= mouse[0] <= 280 + play_w and 275 <= mouse[1] <= 275 + play_h:
            # scaling the original back button
            screen.blit(play_hover, (280 - (play_hover_size[0] - play_w) // 2,
                                     275 - (play_hover_size[1] - play_h) // 2))
        else:
            # if not hovering, then show the original play button

            screen.blit(play, (280,275))

        # Shop button with hover effect
        if 105 <= mouse[0] <= 105 + shop_w and 420 <= mouse[1] <= 420 + shop_h:
            screen.blit(shop_hover, (105 - (shop_hover_size[0] - shop_w) // 2,
                                     420 - (shop_hover_size[1] - shop_h) // 2))
        else:
            screen.blit(shops, (105, 420))

        # Credit button with hover effect
        if 105 <= mouse[0] <= 105 + credit_w and 520 <= mouse[1] <= 520 + credit_h:
            screen.blit(credit_hover, (105 - (credit_hover_size[0] - credit_w) // 2,
                                       520 - (credit_hover_size[1] - credit_h) // 2))
        else:
            screen.blit(credit, (105, 520))

        # Option button with hover effect
        if 505 <= mouse[0] <= 505 + option_w and 420 <= mouse[1] <= 420 + option_h:
            screen.blit(option_hover, (505 - (option_hover_size[0] - option_w) // 2,
                                       420 - (option_hover_size[1] - option_h) // 2))
        else:
            screen.blit(option, (505, 420))

        # Rules button with hover effect
        if 505 <= mouse[0] <= 505 + rules_w and 520 <= mouse[1] <= 520 + rules_h:
            screen.blit(rules_hover, (505 - (rules_hover_size[0] - rules_w) // 2,
                                      520 - (rules_hover_size[1] - rules_h) // 2))
        else:
            screen.blit(rules, (505, 520))

        # Quit button with hover effect
        if 280 <= mouse[0] <= 280 + quit_w and 600 <= mouse[1] <= 600 + quit_h:
            screen.blit(quit_hover, (280 - (quit_hover_size[0] - quit_w) // 2,
                                     600 - (quit_hover_size[1] - quit_h) // 2))
        else:
            screen.blit(quit, (280, 600))


        for ev in pygame.event.get():

            # getting the mouse position (future need)
            mouse = pygame.mouse.get_pos()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                print(mouse[0], mouse[1])
            # seeing if the user hits the red x button
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Quit button
                if 280 <= mouse[0] <= 280 + quit_w and 600 <= mouse[1] <= 600 + quit_h:
                    pygame.quit()

                # Credits button
                if 105 <= mouse[0] <= 105 + credit_w and 520 <= mouse[1] <= 520 + credit_h:
                    credits_()

                # Wilderness game button (Play button)
                if 280 <= mouse[0] <= 280 + play_w and 275 <= mouse[1] <= 275 + play_h:
                    status = wilderness_explorer(player, player2)
                    if status:
                        players = initiate_players()
                        player = players[0]
                        player2 = players[1]

                # Shop button
                if 105 <= mouse[0] <= 105 + shop_w and 420 <= mouse[1] <= 420 + shop_h:
                    shop(player, player2)

                # Options button
                if 505 <= mouse[0] <= 505 + option_w and 420 <= mouse[1] <= 420 + option_h:
                    under_construction()

                # Rules button
                if 505 <= mouse[0] <= 505 + rules_w and 520 <= mouse[1] <= 520 + rules_h:
                    rules_()

        # update the display so that the loop changes will appear
        pygame.display.update()

# Under construction screen
def credits_():
    screen = pygame.display.set_mode(resolution)

    # in order to print something we need to first create a font, create the text and then blit

    # creating the fonts:
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

    # creating the rendered texts for the credits
    augusto_text = comicsansfont.render("Augusto Santos, ajrsantos@novaims.unl.pt", True, white)
    diogo_text = comicsansfont.render("Diogo Rastreio, drasteiro@novaims.unl.pt", True, white)
    liah_text = comicsansfont.render("Liah Rosenfeld, lrosenfeld@novaims.unl.pt", True, white)

    # main loop to detect user input and display the credits
    while True:
        # getting the position of the users mouse
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checking if the user clicked the back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    interface()

        # display my screen
        screen.fill(deep_black) # we can fill the screen with an image instead of deep_black

        # displaying our texts
        screen.blit(augusto_text, (0,0)) # first line
        screen.blit(diogo_text, (0, 25))
        screen.blit(liah_text, (0, 50))

        # drawing and displaying the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_text = corbelfont.render("back", True, white)
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # updating the display
        pygame.display.update()


def rules_():

    # setting up the background
    background = pygame.image.load("ui/background.png")
    # para que o background ocupe toda a tela
    background = pygame.transform.scale(background, (width, height))

    back = pygame.image.load("ui/back.png")
    rules = pygame.image.load("ui/rules.png")

    # Initial back button size
    back_width, back_height = back.get_width(), back.get_height()
    back_hover_size = (int(back_width * 1.3), int(back_height * 1.3))

    # screen setup:
    screen = pygame.display.set_mode(resolution)

    # main loop to detect user input and display the credits
    cont = True
    while cont:
        screen.blit(background, (0, 0))  # 0,0 will fill the entire screen
        screen.blit(rules,(100,100)) # putting rules img on the screen

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

            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checking if the user clicked the back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= mouse[0] <= 100 and 10 <= mouse[1] <= 50:
                    cont = False

        # pygame.draw.rect(screen, dark_red, [0, 0, 90, 30])
        # updating the display
        pygame.display.update()



def wilderness_explorer(player, player2):
    status = game_loop(player, player2)
    if status:
        return True
