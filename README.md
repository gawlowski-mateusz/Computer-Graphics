# Computer-Graphics

This project showcases various OpenGL rendering techniques by demonstrating a 3D egg model created with points, lines, and triangles. The project includes features such as coloring, texturing, and interactive camera controls. The egg is textured with a custom image, adding a personalized touch to the rendering.

## Features

### 1. Egg Creation
The egg model is generated using different primitive types:
- **Points**: The egg is initially created using points to define its surface.
- **Lines**: Lines are used to connect the points, giving a wireframe view of the egg.
- **Triangles**: Finally, the surface of the egg is formed using triangles, providing a solid 3D object.

### 2. Coloring the Egg
The egg is rendered with colors to enhance its visual appeal. Each vertex of the egg can be assigned a color, which is then interpolated across the surface to create a smooth gradient effect.

### 3. Interactive Camera Control
- **Mouse Rotation**: Users can rotate the camera around the egg using the mouse. This allows for an interactive exploration of the 3D model from different angles.
- **Zooming**: The right mouse button is used to zoom in and out. This feature lets users examine the egg closely or view it from a distance.
- **Zoom Limiting**: To prevent excessive zooming, the zoom level is constrained within certain limits, ensuring a comfortable viewing experience.

### 4. Texturing the Egg
The egg can be textured with a custom image. In this project, a unique feature is the ability to apply even your own face as a texture on the egg. This involves mapping a 2D image onto the 3D surface of the egg, giving it a personalized and realistic appearance.

## Overview

This project demonstrates the following key concepts and techniques in OpenGL:
- Setting up an OpenGL context using GLFW.
- Compiling and linking vertex and fragment shaders.
- Creating and managing vertex buffer objects (VBOs) and vertex array objects (VAOs).
- Applying GLSL shaders for color and texture mapping.
- Implementing interactive controls for camera manipulation.
- Using transformation matrices to handle object and camera movements.

## Project Structure

- `main.py`: The main script that sets up the OpenGL context, compiles shaders, initializes buffers, and handles rendering and user input.
- `shader_compiler.py`: A helper script for compiling vertex and fragment shaders from source code.
- `buffers.py`: Manages the creation and binding of vertex buffer objects (VBOs) and vertex array objects (VAOs).
- `transformations.py`: Contains functions for creating transformation matrices (model, view, projection) using GLM.
- `window.py`: Initializes GLFW, creates a window, and handles user input.
- `requirements.txt`: Lists the Python dependencies required for this project.

## Installation and Setup

To run this project, you'll need:
- Python 3.6 or higher
- Pip for managing Python packages

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/opengl-egg-rendering.git
    cd opengl-egg-rendering
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure your system has the necessary OpenGL drivers and libraries installed. On Ubuntu, you can install the necessary packages with:
    ```bash
    sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev
    ```

## Running the Project

To run the project, simply execute example script:
```bash
python script.py
```

## Dependencies

The project depends on the following Python packages:
- `glfw`: For creating windows, contexts, and managing input.
- `PyOpenGL`: Python bindings for OpenGL.
- `numpy`: For efficient array manipulation.
- `pyglm`: For matrix and vector operations (GLM bindings for Python).

These can be installed using the provided `requirements.txt` file.

## Additional Information

- Ensure your graphics drivers are up to date to support modern OpenGL features.
- The script uses OpenGL 3.3 core profile. Make sure your hardware supports this version.

## Acknowledgments

- The OpenGL community and documentation.
- Various online tutorials and references on OpenGL and GLFW.