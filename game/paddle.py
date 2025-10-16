import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed=7):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def center_y(self):
        return self.y + self.height / 2

    def auto_track(self, ball, screen_height, max_step=None, error=0):
        """
        Simple AI: follow the ball center with optional speed cap and small error.
        max_step: cap per-frame movement (defaults to self.speed)
        error:   small offset to make AI fallible (e.g., +/- 6)
        """
        if max_step is None:
            max_step = self.speed

        target = (ball.y + ball.height / 2) + error
        cy = self.center_y()
        dy = 0
        if target < cy:
            dy = -min(max_step, cy - target)
        elif target > cy:
            dy = min(max_step, target - cy)
        self.move(dy, screen_height)
