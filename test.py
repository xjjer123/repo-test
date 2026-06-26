import pygame
import random

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 设置屏幕大小
size = (400, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("俄罗斯方块")

# 定义方块大小
block_size = 20

# 方块形状定义
SHAPES = [
    [[1, 1], [1, 1]],  # I型
    [[1, 1, 0], [0, 1, 1]],  # L型
    [[0, 1, 1], [1, 1, 0]],  # 反L型
    [[1, 1, 1], [0, 1, 0]],  # T型
    [[1, 1], [1, 0], [1, 0]],  # S型
    [[0, 1, 1], [1, 1, 0]],  # Z型
    [[1, 1, 1], [1, 0, 0]]   # J型
]

# 随机选择一个方块
def get_shape():
    return SHAPES[random.randint(0, len(SHAPES) - 1)]

# 移动方块
def move_down(shape, grid):
    for i in range(len(shape)):
        shape[i][1] += 1
    return shape

# 检查碰撞
def check_collision(shape, grid):
    for i in range(len(shape)):
        x, y = shape[i]
        if y >= len(grid) or x < 0 or x >= len(grid[0]) or grid[y][x]:
            return True
    return False

# 清除完成的行
def clear_lines(grid):
    lines_cleared = 0
    new_grid = []
    for row in grid:
        if 0 not in row:  # 如果一行没有空格，则该行已满
            lines_cleared += 1
    if lines_cleared > 0:
        for _ in range(lines_cleared):
            new_grid.insert(0, [0]*len(grid[0]))
    else:
        new_grid.extend(grid)
    return new_grid, lines_cleared

# 主函数
def main():
    clock = pygame.time.Clock()
    grid = [[0 for _ in range(10)] for _ in range(20)]
    current_shape = get_shape()
    current_x = int((len(grid[0]) - len(current_shape)) / 2)
    current_y = 0
    game_over = False

    while not game_over:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    current_x += 1
                elif event.key == pygame.K_DOWN:
                    current_y += 1
                elif event.key == pygame.K_UP:
                    current_shape = rotate_shape(current_shape)

        # 移动方块
        current_y += 1
        if check_collision(move_down(current_shape, grid), grid):
            current_y -= 1
            for i in range(len(current_shape)):
                x, y = current_shape[i]
                x += current_x
                y += current_y
                grid[y][x] = 1
            current_shape = get_shape()
            current_x = int((len(grid[0]) - len(current_shape)) / 2)
            current_y = 0

        grid, lines_cleared = clear_lines(grid)
        if lines_cleared > 0:
            for _ in range(lines_cleared):
                screen.fill(WHITE)
                draw_grid(grid)
                pygame.display.flip()
                pygame.time.wait(500)

        draw_grid(grid)
        draw_current_shape(current_shape, current_x, current_y)
        pygame.display.flip()
        clock.tick(2)

    pygame.quit()

def rotate_shape(shape):
    return list(zip(*shape[::-1]))

def draw_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x]:
                pygame.draw.rect(screen, WHITE, [(x * block_size) + 1, (y * block_size) + 1, block_size - 2, block_size - 2])

def draw_current_shape(shape, x, y):
    for i in range(len(shape)):
        x1, y1 = shape[i]
        pygame.draw.rect(screen, RED, [(x1 + x) * block_size + 1, (y1 + y) * block_size + 1, block_size - 2, block_size - 2])

if __name__ == "__main__":
    main()
