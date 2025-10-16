import sys
import random
import pygame

# initialize mixer before pygame for low-latency sound
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

# import the engine from the package (use package-relative import so
# running `python -m ping-pong.main` works)
from .game.game_engine import GameEngine

WIDTH, HEIGHT = 960, 540
FPS = 60


def main():
    random.seed()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Ping Pong")
    clock = pygame.time.Clock()

    engine = GameEngine(WIDTH, HEIGHT)

    running = True
    paused = False

    while running:
        # handle system events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        # update & draw
        if not paused and not engine.game_over:
            engine.handle_input()
            engine.update()

        engine.render(screen)

        # if someone won, show replay menu (blocks until user chooses)
        if engine.game_over:
            engine.show_replay_menu(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
