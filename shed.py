import pygame 
from config import *
from utils import *

def shed(player):
    # setting the background 
    background = pygame.image.load("images/puppy.jpg")

    # setting the background into our selected resolution
    background = pygame.transform.scale(background, resolution)

    # setting the screen
    screen = pygame.display.set_mode(resolution)

    # setting the clock for fps
    clock = pygame.time.Clock()

    #since i left the previous area from the righr, here i will start from the left
    player.rect.left = 0

    #creating the player group and adding a player to it
    player_group = pygame.sprite.Group()
    player_group.add(player)

    #setting up the shed area as a special area in the shed map location 
    special_area = pygame.Rect(530, 30, 140, 140)

    #normal main game loop (becouse reasons, shed area will not have enemies nor bullits)
    #this is our base implementation and you are allowed to change it!!!!
    running = True
    while running:
        clock.tick(fps)
        #displaying the background on the entirety of the screen
        screen.blit(background, (0, 0))

        #allowing the player to quit
        for event in pygame.event.get():  #É um for porque para cada evento que acontece (clicar, mover...), ele vai verificar se é o evento de sair do jogo
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #updating the player position
        player_group.update()

        #detect if the user walked into the special area 
        if special_area.colliderect(player.rect):
            #if the player walked into the special area, we will return to the under construction screen
            under_construction()

            #changing the player position
            player.rect.left = 200
            player.rect.top = 560

        #allowing the player to return back to the previous area 
        if player.rect.left <= 0:
            #podition the player to the right of the screen
            player.rect.left = width - player.rect.width

            #switching back to the main game 
            return "main"
        
        #drawing the player
        player_group.draw(screen)
        #updating the display
        pygame.display.flip()