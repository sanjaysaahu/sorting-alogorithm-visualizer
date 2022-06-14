import pygame
import random
import math

pygame.init()


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE
    SIDE_PAD = 100
    TOP_PAD = 150
    GRADIENT = [
        (207, 159, 255),
        (224, 176, 255),
        (218, 112, 214)
    ]

    FONT = pygame.font.SysFont('comicsans', 18)
    LARGE_FONT = pygame.font.SysFont("comicsans", 25)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_lst(lst)

    def set_lst(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def generate_lst(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def draw(draw_info, sorting_algorithm_name):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{sorting_algorithm_name}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting ", 1,
                                     draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 35))

    sorting = draw_info.FONT.render(f"B - Bubble sort | I - Insertion sort | Q - Quick sort | Up -Incr speed | Down - Decr speed", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, ((draw_info.width / 2 - sorting.get_width() / 2), 60))

    draw_lst(draw_info)
    pygame.display.update()


def draw_lst(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIENT[i % 3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg == True:
        pygame.display.update()


def bubble_sort(draw_info):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            num1 = lst[j]
            num2 = lst[j + 1]
            if num1 > num2:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_lst(draw_info, {j: draw_info.RED, j + 1: draw_info.GREEN}, True)
                yield True
    return lst


def insertion_sort(draw_info):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        key = lst[i]
        draw_lst(draw_info, {i: draw_info.RED}, True)
        yield True
        j = i - 1
        while j >= 0 and key < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1

        lst[j + 1] = key
        draw_lst(draw_info, {j + 1: draw_info.GREEN}, True)
        yield True
    return lst


# This function is same in both iterative and recursive
def partition(lst, l, h):
    i = (l - 1)
    x = lst[h]

    for j in range(l, h):
        if lst[j] <= x:
            # increment index of smaller element
            i = i + 1
            lst[i], lst[j] = lst[j], lst[i]

    lst[i + 1], lst[h] = lst[h], lst[i + 1]
    return (i + 1)


# Function to do Quick sort
# lst[] --> lstay to be sorted,
# l  --> Starting index,
# h  --> Ending index
def quick_sort(draw_info, l=0, h=49):
    # Create an auxiliary stack
    lst = draw_info.lst
    size = h - l + 1
    stack = [0] * (size)

    # initialize top of stack
    top = -1

    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    # Keep popping from stack while is not empty
    while top >= 0:

        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted lst
        p = partition(lst, l, h)
        draw_lst(draw_info, {h: draw_info.RED, p: draw_info.GREEN}, True)
        yield True

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h


def main():
    running = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 2
    max_val = 200
    lst = generate_lst(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    speed = 10
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble sort"
    sorting_algorithm_generator = None
    while running:
        clock.tick(speed)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_lst(n, min_val, max_val)
                draw_info.set_lst(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info)
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick sort"
            elif event.key == pygame.K_UP:
                speed += 2
            elif event.key == pygame.K_DOWN and speed > 2:
                speed -= 2



    pygame.quit()


if __name__ == "__main__":
    main()
