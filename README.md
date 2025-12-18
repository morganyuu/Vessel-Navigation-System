# Vessel Navigation Simulator

## Description

The Vessel Navigation Simulator is a console-based Python application that models the movement of a vessel across the Earth’s surface. Users can set waypoints, calculate distances between geographic coordinates, and simulate navigation toward a destination while accounting for random environmental effects.

The program demonstrates how geographic calculations, randomness, and user interaction can be combined to create a simple navigation simulation.

---

## Features

- Interactive console menu
- Latitude and longitude input with validation
- Great-circle distance calculations
- Incremental movement toward a waypoint
- Random wave events that alter vessel position
- Storm countdown that limits available moves
- Clear status reporting after each navigation step

---

## How It Works

1. The user enters the vessel’s starting GPS coordinates.
2. A waypoint can be set anywhere on the globe.
3. Each movement step advances the vessel toward the waypoint.
4. After moving, there is a chance the vessel is hit by a wave and pushed off course.
5. The remaining distance to the waypoint and storm countdown are displayed.
6. The simulation ends when:
   - The vessel reaches the waypoint, or
   - The storm arrives, or
   - The user exits the console.

---

## Technologies Used

- Python 3
- Standard library modules:
  - `math`
  - `random`
