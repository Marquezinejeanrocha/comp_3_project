import pygame
from config import *
import cv2
import sys
import sounds

# Global variable to control if the video has already been shown
video_shown = False

def game_over(player, player2):
    player.save_player_data("save_player_data.json")
    player2.save_player_data("save_player_2_data.json")
    global video_shown
    sounds.background_sound.stop()
    # Creating the screen
    screen = pygame.display.set_mode(resolution)

    # Check if the video has already been shown
    if not video_shown:
        video_path = "images/star_wars_video_2.mp4"
        audio_path = "images/star_wars_audio.mp3"
        cap = cv2.VideoCapture(video_path)

        # Start playing the audio
        audio = pygame.mixer.Sound(audio_path)
        audio.play()

        # Main loop
        running = True
        clock = pygame.time.Clock()

        # Standard while True loop
        while running:
            # Getting mouse position
            mouse = pygame.mouse.get_pos()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # Checking if the back button was clicked
                    if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80:
                        cap.release()
                        audio.stop()
                        video_shown = True  # Update the variable to indicate that the video has been shown
                        return

            # Read a frame from the video
            ret, frame = cap.read()

            # Check if the video has ended
            if not ret:
                print("End of video.")
                cap.release()
                pygame.mixer.music.stop()
                player.respawn()
                player2.respawn()
                video_shown = True  # Update the variable to indicate that the video has been shown
                #interface.interface()
                return "exit"

            # Convert the frame from BGR (OpenCV) to RGB (Pygame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a Pygame Surface
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.rotate(frame, -90)  # Rotate 90 degrees (optional)
            frame = pygame.transform.flip(frame, True, False)  # Flip the image horizontally
            frame = pygame.transform.scale(frame, resolution)  # Scale to screen size

            # Draw the frame on the screen
            screen.blit(frame, (0, 0))
            pygame.display.update()

            # Set the frame rate (FPS)
            clock.tick(24)

        # Release resources
        cap.release()
        pygame.mixer.music.stop()
        pygame.quit()