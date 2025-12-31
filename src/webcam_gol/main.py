import pygame
import cv2
import numpy as np
from scipy.signal import convolve2d

# config
MAX_GRID_SIZE = 400
WINDOW_SIZE = 800
FPS = 30

ALIVE = 1
DEAD = 0

# funcs
def scaledown(arr):
    while arr.shape[0] > MAX_GRID_SIZE or arr.shape[1] > MAX_GRID_SIZE:
        arr = arr[::2, ::2]
    return arr

def squarify(arr):
    h, w = arr.shape
    n = max(h, w)
    pad_top = (n - h) // 2
    pad_bottom = n - h - pad_top
    pad_left = (n - w) // 2
    pad_right = n - w - pad_left
    return np.pad(arr, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant')

"""
This is my initial implementation of the rules of the game of life. It was slow and unoptomized, but proved to be a workable stand in
until I made an optimized implementation. It used inefficient python list to store gamestate instead of NumPy arrays. New generation are
created with python list acesses instead of SciPy convolution.

def next_generation_old(grid):
    copy_grid = []

    for i in range(len(grid)):
        copy_grid.append([])
        for j in range(len(grid[0])):
            copy_grid[i].append(action(grid, i, j))
    return copy_grid

def sum_neighbors(grid, i, j):
    sum = 0

    for a in range(-1,2):
        for b in range(-1,2):
            try:
                if a != 0 or b != 0:
                    if grid[i + a][j + b] != 0:
                        sum += 1
            except:
    return sum

def action(grid, i, j):
    sum = sum_neighbors(grid, i, j)
    place = grid[i][j]

    if sum < 2 and place == 1:
        return 0
    elif (sum == 2 or sum == 3) and place == 1:
        return 1
    elif sum > 3 and place == 1:
        return 0
    elif sum == 3 and place == 0:
        return 1
    return 0
"""








kernel = np.array([[1,1,1],
                   [1,0,1],
                   [1,1,1]])

def next_generation(grid):
    # Count neighbors for each cell
    neighbors = convolve2d(grid, kernel, mode='same', boundary='fill', fillvalue=0)
    # Apply Game of Life rules
    return ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(np.uint8)

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE + 250, WINDOW_SIZE))
    pygame.display.set_caption("Webcam → Game of Life")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 16)

    # webcam settup
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    # game state init
    game_grid = None
    mode = "camera"  # "camera" or "game"
    paused = False

    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if mode == "camera":
                        mode = "game"
                        paused = False
                    elif mode == "game":
                        paused = not paused
                elif event.key == pygame.K_r:
                    mode = "camera"
                    game_grid = None
                    paused = False

        # Capture webcam frame
        ret, frame = cap.read()
        if not ret:
            continue

        # Flip to correct mirror
        frame = cv2.flip(frame, 1)

        # Process frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_small = scaledown(gray)
        frame_small = squarify(frame_small)
        live_frame = (frame_small > 128).astype(np.uint8)

        # Game logic
        if mode == "camera":
            game_grid = live_frame.copy()
            display = cv2.resize(game_grid * 255, (WINDOW_SIZE, WINDOW_SIZE), interpolation=cv2.INTER_NEAREST)
        else:  # Game of Life mode
            if game_grid is None:
                game_grid = live_frame.copy()
            if not paused:
                # Live-reactive: incorporate new pixels as alive cells
                game_grid = next_generation(game_grid | live_frame)
            display = cv2.resize(game_grid * 255, (WINDOW_SIZE, WINDOW_SIZE), interpolation=cv2.INTER_NEAREST)

        # Convert to pygame surface
        display_rgb = cv2.cvtColor(display, cv2.COLOR_GRAY2RGB)
        display_surface = pygame.surfarray.make_surface(np.transpose(display_rgb, (1, 0, 2)))

        # Draw to screen
        screen.fill((255, 255, 255))
        screen.blit(display_surface, (0, 0))

        # Draw instructions
        instructions = [
            "How to use:",
            "",
            "• Press SPACE to start/pause",
            "• Press R to reset to camera",
            "",
            f"Mode: {mode.upper()}",
            f"Paused: {paused if mode == 'game' else 'N/A'}",
            "",
            "",
            "",
            "The pixelated webcam view",
            "feeds the simulation.",
            "",
            "Moving objects in front of",
            "the camera will create new cells."
        ]

        y_offset = 20
        for line in instructions:
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (WINDOW_SIZE + 20, y_offset))
            y_offset += 25

        pygame.display.flip()
        clock.tick(FPS)

    # Cheekey quit sequence
    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()