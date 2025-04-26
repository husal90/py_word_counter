# Python Flask Word Counter

A simple web application built with Python (Flask) and a basic HTML/Tailwind CSS/JavaScript frontend that counts the number of words in a given text input.

## Description

This application provides a user-friendly web interface where users can paste or type text into a text area. Upon clicking the "Count Words" button, the text is sent to a Python Flask backend API endpoint, which processes the text, counts the words using regular expressions, and returns the count. The result is then displayed dynamically on the webpage.

## Features

* Simple and clean user interface using Tailwind CSS.
* Text area for user input.
* Counts words based on sequences of alphanumeric characters (handles basic punctuation).
* Asynchronous request handling using JavaScript `fetch` API.
* Displays the word count dynamically without page reload.
* Basic error handling for empty input and server errors.
* Responsive design for different screen sizes.

## Requirements

* Python 3.x
* Flask library

## Installation

1.  **Clone or Download:** Get the `app.py` file onto your local machine.
2.  **Install Dependencies:** Open your terminal or command prompt, navigate to the directory containing `app.py`, and install Flask:
    ```bash
    pip install Flask
    ```
    *(If you use a virtual environment, activate it first)*

## Usage

1.  **Run the Application:** In your terminal, navigate to the directory containing `app.py` and run the script:
    ```bash
    python app.py
    ```
2.  **Access the App:** Open your web browser and go to the URL provided in the terminal (usually `http://127.0.0.1:5000/` or `http://localhost:5000/`).
3.  **Count Words:**
    * Enter or paste text into the text area.
    * Click the "Count Words" button.
    * The word count will appear below the button.

## Technology Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, Tailwind CSS, JavaScript
* **Word Counting Logic:** Python `re` module (regular expressions)
