--- 

# AIResumeCraft


## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Ai-Resume-Craft
   ```

2. Navigate into the project directory:

   ```bash
   cd crew-ai-webapp
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the FastAPI application:

   ```bash
   fastapi dev main.py
   ```

2. Access the application in your web browser at [http://localhost:8000](http://localhost:8000).

## Project Structure

- **main.py**: Contains the FastAPI application code.
- **static/**: Directory to store static files (e.g., CSS, JavaScript, images).
- **templates/**: Directory to store Jinja2 HTML templates.
- **routes/router.py** : Contains route definitions organized using FastAPI routers.
- **utils** : Contains Different files used for creating agents,tasks and helpers.
- **frames** : Contains Different Frames available.

## How It Works

- **main.py**: This file initializes the FastAPI application and mounts the static directory to serve static files. It includes routes from the router module using app.include_router().
- **templates/home.html**: This HTML template file is rendered when accessing the root URL (`/`). It receives the message variable from the route and displays it on the webpage.
- **static/**: This directory is used to store static files like CSS, JavaScript, or images. The "/static" endpoint is mounted to serve files from this directory.
- **routes/router.py**: This module defines additional routes using FastAPI routers. These routers can be organized based on logical grouping or feature sets.

---
