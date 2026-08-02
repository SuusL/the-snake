from random import choice, randint

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
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс объектов на игровом поле."""

    def __init__(self,
                 body_color: tuple | None = None) -> None:
        self.position = ((GRID_WIDTH / 2) * GRID_SIZE,
                         (GRID_HEIGHT / 2) * GRID_SIZE)
        self.body_color = body_color

    def draw(self) -> None:
        """Заглушка отрисовки объектов на игровом поле."""
        pass


class Apple(GameObject):
    """Класс объекта Яблоко на игровом поле."""

    def __init__(self,
                 body_color: tuple = APPLE_COLOR) -> None:
        super().__init__(body_color)

    def randomize_position(self) -> None:
        """Задает произвольное положение яблока на игровом поле."""
        # единица вычитается чтобы яблоко не оказывалось за пределами поля
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    # Метод draw класса Apple
    def draw(self) -> None:
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс объекта Змейка на игровом поле."""

    def __init__(self,
                 length: int = 1,
                 direction: tuple = RIGHT,
                 next_direction: tuple | None = None,
                 body_color: tuple = SNAKE_COLOR,
                 last: tuple | None = None) -> None:
        super().__init__(body_color)
        self.length = length
        self.positions = [self.position]
        self.direction = direction
        self.next_direction = next_direction
        self.last = last

    def get_head_position(self) -> tuple:
        """Возвращает положение головы Змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Перемещает Змейку по игровому полю."""
        head_position = self.get_head_position()
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.remove(self.last)

    def draw(self) -> None:
        """Отрисовывет Змейку на игровом поле."""
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

    def update_direction(self) -> None:
        """Обновляет направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self) -> None:
        """Перезапускает Змейку с начальными параметрами."""
        self.length = 1
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.positions = [
            ((GRID_WIDTH / 2) * GRID_SIZE, (GRID_HEIGHT / 2) * GRID_SIZE)
        ]
        self.direction = choice([UP, RIGHT, DOWN, LEFT])


def handle_keys(game_object) -> None:
    """Обрабатывает действия пользователя."""
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


def main() -> None:
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.draw()
        apple.draw()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        for position in snake.positions[1:]:
            if position == snake.get_head_position():
                snake.reset()
        snake.move()
        pygame.display.update()


if __name__ == '__main__':
    main()
