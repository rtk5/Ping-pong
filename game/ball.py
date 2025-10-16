import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height,
                 snd_paddle=None, snd_wall=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # optional sounds
        self.snd_paddle = snd_paddle
        self.snd_wall = snd_wall

        # safety cap if you later increase speeds
        self.max_speed = 11

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def _apply_speed_cap(self):
        self.velocity_x = max(-self.max_speed, min(self.max_speed, self.velocity_x))
        self.velocity_y = max(-self.max_speed, min(self.max_speed, self.velocity_y))

    def move(self):
        # integrate position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # top/bottom wall bounce with nudge & sound
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            if self.snd_wall:
                self.snd_wall.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            if self.snd_wall:
                self.snd_wall.play()

    def check_collision(self, player, ai):
        """Rectangle overlap check with de-sticking and angle variation."""
        ball_rect = self.rect()

        # vs player paddle
        if ball_rect.colliderect(player.rect()):
            # nudge out to avoid immediate re-collide
            self.x = player.rect().right
            # reflect X; add a bit of "spin" from impact position
            offset = ((self.y + self.height / 2) - player.center_y()) / (player.height / 2)
            self.velocity_x = abs(self.velocity_x) + 0.5
            self.velocity_y += offset * 3
            self._apply_speed_cap()
            if self.snd_paddle:
                self.snd_paddle.play()

        # vs AI paddle
        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.rect().left - self.width
            offset = ((self.y + self.height / 2) - ai.center_y()) / (ai.height / 2)
            self.velocity_x = -abs(self.velocity_x) - 0.5
            self.velocity_y += offset * 3
            self._apply_speed_cap()
            if self.snd_paddle:
                self.snd_paddle.play()

    def reset(self):
        """Center ball and flip serve side; randomize vertical a bit."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
