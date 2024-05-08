---

# Crew AI Demo Web-App

This is a Demo Web-App for OC training

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Oc-training/crew-ai-webapp
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
   uvicorn main:app --reload
   ```

2. Access the application in your web browser at [http://localhost:8000](http://localhost:8000).

## Project Structure

- **main.py**: Contains the FastAPI application code.
- **static/**: Directory to store static files (e.g., CSS, JavaScript, images).
- **templates/**: Directory to store Jinja2 HTML templates.
- **routes/router.py** : Contains route definitions organized using FastAPI routers.

## How It Works

- **main.py**: This file initializes the FastAPI application, mounts the static directory to serve static files, and configures Jinja2Templates for rendering HTML templates. It defines a single route at `/` that renders the `home.html` template, passing a message variable to the template context.
- **templates/home.html**: This HTML template file is rendered when accessing the root URL (`/`). It receives the message variable from the route and displays it on the webpage.

---
