import pygame, sys, time, random

# Game settings
class Settings:
    difficulty = 20
    frame_size_x = 720
    frame_size_y = 480

# Colors (R, G, B)
class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

# Initialize Pygame
pygame.init()

class Game:
    def __init__(self):
        self.check_errors()
        self.init_window()
        self.init_game_variables()
        self.main_loop()

    def check_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initializing game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialized')

        
    def init_window(self):
        pygame.display.set_caption('Snake Game')
        self.game_window = pygame.display.set_mode((Settings.frame_size_x, Settings.frame_size_y))
        self.fps_controller = pygame.time.Clock()

    def init_game_variables(self):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = self.random_food_pos()
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def random_food_pos(self):
        return [random.randrange(1, (Settings.frame_size_x // 10)) * 10, random.randrange(1, (Settings.frame_size_y // 10)) * 10]

    def game_over(self):
        my_font = pygame.font.SysFont('Cambria', 90)
        game_over_surface = my_font.render('Game Over', True, Colors.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (Settings.frame_size_x / 2, Settings.frame_size_y / 4)
        self.game_window.fill(Colors.black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(0, Colors.red, 'times', 20)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (Settings.frame_size_x / 10, 15)
        else:
            score_rect.midtop = (Settings.frame_size_x / 2, Settings.frame_size_y / 1.25)
        self.game_window.blit(score_surface, score_rect)

    def main_loop(self):
        while True:
            self.event_handler()
            self.update_snake_direction()
            self.move_snake()
            self.snake_body_mechanism()
            self.check_game_over()
            self.update_screen()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update_snake_direction(self):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move_snake(self):
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

    def snake_body_mechanism(self):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()
        if not self.food_spawn:
            self.food_pos = self.random_food_pos()
        self.food_spawn = True

    def check_game_over(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > Settings.frame_size_x - 10:
            self.game_over()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > Settings.frame_size_y - 10:
            self.game_over()
        for block in self.snake_body[1:]:
            if self.snake_pos == block:
                self.game_over()

    def update_screen(self):
        self.game_window.fill(Colors.black)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, Colors.green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.game_window, Colors.white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
        self.show_score(1, Colors.white, 'times new roman', 20)
        pygame.display.update()
        self.fps_controller.tick(Settings.difficulty)

if __name__ == "__main__":
    Game()
