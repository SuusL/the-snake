"""Модуль содержит классы и функции
для запуска игры Змейка.
"""


from random import choice, randint

import pygame as pg

# константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# цвет фона
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# цвет границ ячейки
BORDER_COLOR = (93, 216, 228)

# цвет Яблока
APPLE_COLOR = (255, 0, 0)

# цвет Змейки
SNAKE_COLOR = (0, 255, 0)

# скорость движения змейки
SPEED = 20

# настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# заголовок окна игрового поля
pg.display.set_caption('Змейка')

# настройка времени
clock = pg.time.Clock()


class GameObject:
    """Базовый класс объектов на игровом поле."""

    def __init__(self,
                 body_color: tuple | None = None,
                 border_color: tuple | None = None) -> None:
        self.position = SCREEN_CENTER
        self.body_color = body_color
        self.border_color = border_color

    def draw_cell(self,
                  surface,
                  position,
                  size,
                  body_color,
                  border_color) -> None:
        """Отрисовка ячейки на игровом поле."""
        rect = pg.Rect(position, size)
        pg.draw.rect(surface, body_color, rect)
        if border_color:
            pg.draw.rect(surface, border_color, rect, 1)

    def draw(self) -> None:
        """Заглушка отрисовки объектов на игровом поле."""
        raise NotImplementedError('Метод переопредляется в дочерних классах.')


class Apple(GameObject):
    """Класс объекта Яблоко на игровом поле."""

    def __init__(self,
                 occupied_positions: list = [SCREEN_CENTER],
                 body_color: tuple = APPLE_COLOR,
                 border_color: tuple = BORDER_COLOR
                 ) -> None:
        super().__init__(body_color, border_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions) -> None:
        """Задает произвольное положение яблока на игровом поле."""
        while True:
            # единица вычитается чтобы Яблоко не оказывалось за пределами поля
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(screen,
                       self.position,
                       (GRID_SIZE, GRID_SIZE),
                       self.body_color,
                       BORDER_COLOR
                       )


class Snake(GameObject):
    """Класс объекта Змейка на игровом поле."""

    def __init__(self,
                 body_color: tuple = SNAKE_COLOR,
                 border_color: tuple = BORDER_COLOR) -> None:
        super().__init__(body_color, border_color)
        self.length: int = 1
        self.positions: list = [self.position]
        self.direction: tuple = RIGHT
        self.next_direction: tuple | None = None
        self.last: tuple | None = None

    def get_head_position(self) -> tuple:
        """Возвращает положение головы Змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Перемещает Змейку по направлению движения."""
        head_position_x, head_position_y = self.get_head_position()
        new_head_position = (
            (head_position_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self) -> None:
        """Отрисовывет Змейку на игровом поле."""
        for position in self.positions[:-1]:
            self.draw_cell(screen,
                           position,
                           (GRID_SIZE, GRID_SIZE),
                           self.body_color,
                           BORDER_COLOR
                           )
        # отрисовка головы змейки
        self.draw_cell(screen,
                       self.get_head_position(),
                       (GRID_SIZE, GRID_SIZE),
                       self.body_color,
                       BORDER_COLOR
                       )
        # затирание последнего сегмента
        if self.last:
            self.draw_cell(screen,
                           self.last,
                           (GRID_SIZE, GRID_SIZE),
                           BOARD_BACKGROUND_COLOR,
                           None)

    def update_direction(self) -> None:
        """Обновляет направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self) -> None:
        """Перезапускает Змейку с начальными параметрами."""
        self.length = 1
        self.positions = [
            self.position
        ]
        self.direction = choice([UP, RIGHT, DOWN, LEFT])


def handle_keys(game_object) -> None:
    """Обрабатывает действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
