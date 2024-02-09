import pygame
import random
import time

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
BUTTON_SIZE = 300
BUTTON_MARGIN = 45
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

HIGH_SCORE_FILE = "high_score.txt"

class Button:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.highlighted = False

    def draw(self, screen):
        if self.highlighted:
            pygame.draw.rect(screen, WHITE, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def highlight(self):
        self.highlighted = True

    def reset_highlight(self):
        self.highlighted = False


class SimonGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simon Game")
        self.clock = pygame.time.Clock()
        self.buttons = [
            Button(RED, BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE),
            Button(GREEN, BUTTON_SIZE + 2 * BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE),
            Button(BLUE, BUTTON_MARGIN, BUTTON_SIZE + 2 * BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE),
            Button(YELLOW, BUTTON_SIZE + 2 * BUTTON_MARGIN, BUTTON_SIZE + 2 * BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE)
        ]
        self.pattern = []

    def generate_pattern(self, length):
        self.pattern = [random.choice(self.buttons) for _ in range(length)]

    def display_pattern(self):
        for button in self.pattern:
            button.highlight()
            self.draw_buttons()
            pygame.display.update()
            time.sleep(0.5)
            button.reset_highlight()
            self.draw_buttons()
            pygame.display.update()
            time.sleep(0.5)

    def check_input(self):
        input_sequence = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.rect.collidepoint(mouse_pos):
                            button.highlight()
                            self.draw_buttons()
                            pygame.display.update()
                            time.sleep(0.1)
                            button.reset_highlight()
                            self.draw_buttons()
                            pygame.display.update()
                            input_sequence.append(button)
                            if input_sequence[-1] != self.pattern[len(input_sequence) - 1]:
                                return False
                            if len(input_sequence) == len(self.pattern):
                                return True

    def run(self):
        score = 0
        running = True

        font = pygame.font.Font(None, 36)

        while running:
            self.screen.fill(BLACK)
            text = font.render(f"Score: {score}    High Score: {self.load_high_score()}", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 20))
            self.screen.blit(text, text_rect)

            self.draw_buttons()
            pygame.display.update()

            self.generate_pattern(score + 1)
            self.display_pattern()

            if not self.check_input():
                self.handle_high_score(score)
                print("Game Over! Your score:", score)
                running = False
            else:
                score += 1
                if score > 10:
                    print("Congratulations! You won!")
                    running = False

            self.clock.tick(FPS)

        pygame.quit()
        quit()

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self, score):
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))

    def handle_high_score(self, score):
        high_score = self.load_high_score()
        if score > high_score:
            print("New high score achieved!")
            self.save_high_score(score)
            high_score = score
        print("The high score is:", high_score)

def main():
    pygame.init()
    game = SimonGame()
    game.run()

if __name__ == "__main__":
    main()
