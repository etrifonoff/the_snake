from random import randint

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной класс игры"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """
        Метод отрисовки яблока и змейки,
        будет переопределен в соответствующих классах
        """
        pass


class Apple(GameObject):
    """Класс, описывающий аттрибуты и методы яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод генерирует позицию яблока"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Метод для отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_position(self):
        """
        Метод возвращает текущую позицию яблока.
        Необходим для обработки "поедания" яблока.
        """
        return self.position


class Snake(GameObject):
    """Класс, описывающий аттрибуты и методы змейки"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод, изменения направления змейти при нажатии клавиш"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки"""
        x, y = self.get_head_position()
        dx = GRID_SIZE * self.direction[0]
        dy = GRID_SIZE * self.direction[1]

        head_new = (
            (x + dx),
            (y + dy),
        )

        if head_new[0] < 0:
            head_new = (SCREEN_WIDTH - GRID_SIZE, head_new[1])
        elif head_new[0] >= SCREEN_WIDTH:
            head_new = (0, head_new[1])

        if head_new[1] < 0:
            head_new = (head_new[0], SCREEN_HEIGHT - GRID_SIZE)
        elif head_new[1] >= SCREEN_HEIGHT:
            head_new = (head_new[0], 0)

        self.positions.insert(0, head_new)
        if len(self.positions) > self.length:
            self.positions.pop()

        if self.positions[0] in self.positions[1:]:
            self.reset()

    def draw(self):
        """Метод для отрисовки змейки"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Метод возвращает позицию головы змейки.
        Необходим для обработки "поедания" яблока.
        """
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает параметры змейки"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def eat_apple(self, apple):
        """Метод, описывающий "поедание" яблока"""
        self.positions.insert(0, apple.get_position())

        if self.length == 1:
            self.positions.insert(1, self.get_head_position())

        self.length += 1


def handle_keys(game_object):
    """Функция обработки нажатий клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    # Тут опишите основную логику игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.get_position():
            snake.eat_apple(apple)
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
