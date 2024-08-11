# A* vs Dijkstra Algorithm Visualization

This project is a Python-based visualization tool that compares the A* and Dijkstra pathfinding algorithms using Pygame.

## Features

- Interactive grid-based environment
- Visualization of A* and Dijkstra algorithms
- Real-time comparison of algorithm performance
- User-friendly interface for creating start points, end points, and obstacles

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/astar-dijkstra-visualization.git
   ```
2. Install the required dependencies:
   ```
   pip install pygame
   ```

## Usage

Run the script:
```
python pathfinding_visualizer.py
```

### Controls:
- Left Mouse Button: Place start point, end point, and barriers
- Right Mouse Button: Remove points/barriers
- Spacebar: Start the algorithm visualization
- 'C' key: Clear the grid

## How it works

The program creates a grid where users can set start and end points, as well as obstacles. When initiated, it runs both A* and Dijkstra algorithms, visualizing their path-finding process and displaying the time taken by each algorithm.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
