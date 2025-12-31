# Webcam Game of Life

A real-time interactive implementation of Conway's Game of Life that uses your webcam as input. Move in front of your camera to create living cells and watch them evolve according to the classic Game of Life rules.

## Features

- **Live webcam integration**: Your movements become living cells
- **Real-time simulation**: Watch the Game of Life unfold in real-time
- **Interactive controls**: Start, pause, and reset the simulation
- **Reactive mode**: New movements continuously add cells to the running simulation

## Demo

The program captures your webcam feed, converts it to a binary grid based on brightness, and feeds it into Conway's Game of Life. As you move, new cells are born, creating a dynamic and interactive experience.


### Prerequisites
- Python 3.14 or higher
- Poetry 2.2.1 or higher
- A working webcam

## Usage

Installation:
```bash
poetry install
```

Run the program:
```bash
poetry run webcam-gol
```
Note: The first run may take longer because Python needs to load and initialize some large native libraries and their dependencies. Subsequent runs are much faster thanks to OS-level caching and precompiled bytecode.

### Controls

- **SPACE**: Start the Game of Life simulation (or pause/unpause when running)
- **R**: Reset and return to camera mode

### How It Works

1. The program starts in **camera mode**, showing your pixelated webcam feed
2. Press **SPACE** to switch to **game mode** and start the simulation
3. In game mode, the current frame becomes the initial state
4. The simulation runs according to Conway's Game of Life rules
5. Your continued movements add new living cells to the simulation
6. Press **SPACE** again to pause/unpause
7. Press **R** to reset and return to camera mode

## Game of Life Rules

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


## Technical Details

- Maximum grid size: 400x400 cells
- Window size: 1050x800 pixels (800x800 simulation + 250px info panel)
- Frame rate: 30 FPS
- Brightness threshold: 128 (for converting webcam feed to binary)

## Dependencies

- `pygame`: Game window and rendering
- `opencv-python` (cv2): Webcam capture and image processing
- `numpy`: Array operations and grid management
- `scipy`: Convolution for neighbor counting

All dependencies are automatically installed via Poetry.

## Troubleshooting

**Webcam not working?**
- The program is set to use camera index `1`. If you only have one webcam, change line 48 in `gol.py` to:
  ```python
  cap = cv2.VideoCapture(0)
  ```

**Black screen?**
- Check that your webcam is not being used by another application
- Try adjusting the brightness threshold in the code

**Performance issues?**
- The grid is automatically scaled down to max 400x400
- You can reduce `MAX_GRID_SIZE` for better performance

## License

MIT License - feel free to use and modify as you wish!

## Contributing

Pull requests are welcome! Feel free to open an issue if you find bugs or have suggestions.

## Acknowledgments

Inspired by Conway's Game of Life and the desire to make it interactive and tangible.