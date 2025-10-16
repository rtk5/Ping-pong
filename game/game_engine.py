import pygame
from pathlib import Path
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        # --- sounds ---
        # Make sure pygame.mixer.pre_init / mixer.init were called in main.py
        # Load sounds relative to the package so the game can be started from
        # the parent directory (python -m ping-pong.main). If assets are
        # missing, fall back to None so the game still runs.
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        paddle_path = assets_dir / "paddle.wav"
        wall_path = assets_dir / "wall.wav"
        score_path = assets_dir / "score.wav"

        self.snd_paddle = pygame.mixer.Sound(str(paddle_path)) if paddle_path.exists() else None
        self.snd_wall = pygame.mixer.Sound(str(wall_path)) if wall_path.exists() else None
        self.snd_score = pygame.mixer.Sound(str(score_path)) if score_path.exists() else None

        # Ball receives paddle/wall sounds so it can play on velocity flips
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height,
                         snd_paddle=self.snd_paddle, snd_wall=self.snd_wall)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # match settings & game state
        self.win_target = 5           # default "first to 5"
        self.game_over = False        # becomes True when someone hits win_target
        self.ai_error = 0             # tweak for difficulty if you want
        self.ai_max_step = None       # use paddle.speed by default

    # -------- core loop hooks --------
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # score (left/right). You can switch to rect edges later if you prefer.
        if self.ball.rect().right < 0:
            self.ai_score += 1
            if self.snd_score:
                self.snd_score.play()
            self.ball.reset()
        elif self.ball.rect().left > self.width:
            self.player_score += 1
            if self.snd_score:
                self.snd_score.play()
            self.ball.reset()

        # AI paddle
        self.ai.auto_track(self.ball, self.height, max_step=self.ai_max_step, error=self.ai_error)

        # game-over check using dynamic target
        if self.player_score >= self.win_target or self.ai_score >= self.win_target:
            self.game_over = True

    def render(self, screen):
        # clear background each frame
        screen.fill(BLACK)

        # paddles, ball, midline
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    # -------- game over + replay menu --------
    def new_match(self, win_target):
        """Reset everything for a fresh match with new target."""
        self.win_target = win_target
        self.player_score = 0
        self.ai_score = 0

        # center paddles
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2

        # center ball and alternate serve
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2
        self.ball.velocity_x *= -1
        if self.ball.velocity_y == 0:
            self.ball.velocity_y = 3

        self.game_over = False

    def _draw_center_text(self, screen, lines, pad=16):
        """Utility to draw 1+ centered lines (first big, rest smaller)."""
        title_font = pygame.font.SysFont("Arial", 60)
        body_font = pygame.font.SysFont("Arial", 28)

        screen.fill(BLACK)
        y = self.height // 2

        for i, text in enumerate(lines):
            font = title_font if i == 0 else body_font
            surf = font.render(text, True, WHITE)
            rect = surf.get_rect(center=(self.width // 2, y))
            screen.blit(surf, rect)
            y += rect.height + (pad if i == 0 else pad // 2)

        pygame.display.flip()

    def show_replay_menu(self, screen):
        """
        Blocking replay menu after game_over.
        Keys:
          '3' -> Best of 3 (first to 2)
          '5' -> Best of 5 (first to 3)
          '7' -> Best of 7 (first to 4)
          ESC -> Exit
        """
        # winner title
        if self.player_score >= self.win_target:
            title = "Player Wins!"
        elif self.ai_score >= self.win_target:
            title = "AI Wins!"
        else:
            title = "Match Over"

        self._draw_center_text(
            screen,
            [
                title,
                "Press 3 for Best of 3, 5 for Best of 5, 7 for Best of 7",
                "Press ESC to Exit",
            ],
        )

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.delay(200)
                        pygame.quit()
                        raise SystemExit
                    elif event.key == pygame.K_3:
                        # Best of 3 -> first to 2
                        self.new_match(win_target=2)
                        waiting = False
                    elif event.key == pygame.K_5:
                        # Best of 5 -> first to 3
                        self.new_match(win_target=3)
                        waiting = False
                    elif event.key == pygame.K_7:
                        # Best of 7 -> first to 4
                        self.new_match(win_target=4)
                        waiting = False

            pygame.time.wait(10)
