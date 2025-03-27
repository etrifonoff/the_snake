
import sys
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BOARD_BACKGROUND_COLOR = BLACK

# Цвета границы ячейки, яблока и змейка
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = RED
SNAKE_COLOR = GREEN

# Настройка игрового окна и скорости игры:
SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Основной класс игры."""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки яблока и змейки."""

    def draw_cell(self, position, body_color=None, border_color=BORDER_COLOR):
        """
        Метод для отрисовки одной ячейки на игровом поле.

        Args:
            position: координаты ячейки
            body_color: цвет заполнения ячейки
            border_color: цвет границы ячейки
        """
        # Если цвет не передан, используем цвет объекта
        if body_color is None:
            body_color = self.body_color

        # Создаем прямоугольник и отрисовываем его
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)

        # Отрисовываем границу, если нужно
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс, описывающий аттрибуты и методы яблока."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=None):
        super().__init__(body_color=body_color)
        self.body_color = body_color
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=None):
        """
        Метод генерирует случайную позицию яблока,
        не совпадающую с занятыми клетками.

        Args:
            occupied_cells: список кортежей с координатами занятых клеток.
        """
        if occupied_cells is None:
            occupied_cells = []

        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

            # Если позиция не занята, используем ее
            if new_position not in occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Метод для отрисовки яблока."""
        self.draw_cell(self.position)

    def get_position(self):
        """Метод возвращает текущую позицию яблока."""
        return self.position


class Snake(GameObject):
    """Класс, описывающий аттрибуты и методы змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__()
        self.body_color = body_color
        self.last = None
        self.reset()

    def update_direction(self):
        """Метод, изменения направления змейти при нажатии клавиш."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Метод движения змейки."""
        x, y = self.get_head_position()

        head_new = (
            (x + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH,
            (y + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        )
        self.positions.insert(0, head_new)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод для отрисовки змейки."""
        for position in self.positions[1:]:
            self.draw_cell(position)

        # Отрисовка головы змейки
        self.draw_cell(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(
                self.last, body_color=BOARD_BACKGROUND_COLOR, border_width=0)

    def get_head_position(self):
        """
        Метод возвращает позицию головы змейки.
        Необходим для обработки "поедания" яблока.

        Возвращаемое значение:
            self.positions[0]: позиция головы змейки
        """
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает параметры змейки."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def eat_apple(self, apple_position):
        """Метод, описывающий "поедание" яблока."""
        self.positions.insert(0, apple_position)

        if self.length == 1:
            self.positions.insert(1, self.get_head_position())

        self.length += 1


def handle_keys(game_object):
    """Функция обработки нажатий клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise sys.exit(SystemExit)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pg.init()

    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if (len(snake.positions) > 4
                and snake.get_head_position()) in snake.positions[1:]:
            snake.reset()

        if snake.get_head_position() == apple.get_position():
            snake.eat_apple(apple.get_position())
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
