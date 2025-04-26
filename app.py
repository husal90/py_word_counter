# app.py
# Import necessary libraries from Flask
from flask import Flask, request, jsonify, render_template_string
import re # Import regular expressions for word splitting

# Initialize the Flask application
app = Flask(__name__)

# --- HTML Template ---
# Define the HTML structure, CSS (Tailwind), and JavaScript for the frontend.
# Using render_template_string allows keeping everything in one file for simplicity.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Word Counter</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Add custom styles if needed, or rely purely on Tailwind */
        body {
            font-family: 'Inter', sans-serif; /* Use Inter font */
        }
        /* Basic transition for smoother UI feedback */
        button, textarea {
            transition: all 0.2s ease-in-out;
        }
        /* Style for the result message box */
        #resultBox {
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
            height: 0;
            overflow: hidden;
        }
        #resultBox.visible {
            opacity: 1;
            height: auto; /* Adjust height automatically */
            margin-top: 1rem; /* Add space when visible */
        }
    </style>
     <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body class="bg-gradient-to-r from-blue-100 via-purple-100 to-pink-100 min-h-screen flex items-center justify-center p-4">

    <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-lg">
        <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Word Counter</h1>

        <div class="mb-4">
            <label for="textInput" class="block text-sm font-medium text-gray-700 mb-1">Enter your text below:</label>
            <textarea id="textInput" rows="6"
                      class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm resize-none"
                      placeholder="Type or paste your text here..."></textarea>
        </div>

        <button id="countButton"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
            Count Words
        </button>

        <div id="resultBox" class="mt-6 p-4 bg-green-100 border border-green-300 text-green-800 rounded-lg text-center">
            <p id="resultText" class="font-medium"></p>
        </div>

        <div id="errorBox" class="hidden mt-4 p-3 bg-red-100 border border-red-300 text-red-800 rounded-lg text-center">
             <p id="errorText" class="font-medium"></p>
        </div>
    </div>

    <script>
        // Get references to the HTML elements
        const textInput = document.getElementById('textInput');
        const countButton = document.getElementById('countButton');
        const resultBox = document.getElementById('resultBox');
        const resultText = document.getElementById('resultText');
        const errorBox = document.getElementById('errorBox');
        const errorText = document.getElementById('errorText');

        // --- Event Listener for the Button ---
        countButton.addEventListener('click', async () => {
            const text = textInput.value;

            // Basic validation: Check if text is empty
            if (!text.trim()) {
                showError("Please enter some text to count.");
                return; // Stop execution if input is empty
            }

            // Disable button and show loading state (optional)
            countButton.disabled = true;
            countButton.textContent = 'Counting...';
            hideMessages(); // Hide previous messages

            try {
                // --- API Call to Flask Backend ---
                const response = await fetch('/count', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text }), // Send text in JSON format
                });

                // Check if the request was successful
                if (!response.ok) {
                    // Try to get error message from backend response
                    let errorMsg = `HTTP error! Status: ${response.status}`;
                    try {
                        const errorData = await response.json();
                        errorMsg = errorData.error || errorMsg;
                    } catch (e) {
                        // Ignore if response is not JSON
                    }
                    throw new Error(errorMsg);
                }

                // Parse the JSON response from the backend
                const data = await response.json();

                // --- Display Result ---
                if (data.word_count !== undefined) {
                    resultText.textContent = `Word Count: ${data.word_count}`;
                    resultBox.classList.add('visible'); // Make result box visible
                    errorBox.classList.add('hidden'); // Ensure error box is hidden
                } else if (data.error) {
                     showError(data.error); // Show error from backend
                }

            } catch (error) {
                // --- Handle Network or Other Errors ---
                console.error('Error counting words:', error);
                 showError(`An error occurred: ${error.message}`);
            } finally {
                // Re-enable button and restore text regardless of success or failure
                countButton.disabled = false;
                countButton.textContent = 'Count Words';
            }
        });

        // --- Helper Functions ---
        function showError(message) {
            errorText.textContent = message;
            errorBox.classList.remove('hidden');
            resultBox.classList.remove('visible'); // Hide result box
            resultBox.style.height = '0'; // Collapse result box height
        }

        function hideMessages() {
             errorBox.classList.add('hidden');
             resultBox.classList.remove('visible');
             resultBox.style.height = '0'; // Collapse result box height
        }

        // Hide messages when user starts typing again
        textInput.addEventListener('input', hideMessages);

    </script>

</body>
</html>
"""

# --- Backend Logic ---

def count_words(text):
    """
    Counts the words in a given string.
    Words are sequences of alphanumeric characters.
    Handles potential None input.
    """
    if not text:
        return 0
    # Use regular expression to find sequences of word characters
    # This handles punctuation better than simple splitting by space
    words = re.findall(r'\b\w+\b', text)
    return len(words)

# --- Flask Routes ---

@app.route('/')
def index():
    """
    Serves the main HTML page.
    Uses render_template_string to render the HTML defined above.
    """
    return render_template_string(HTML_TEMPLATE)

@app.route('/count', methods=['POST'])
def handle_count():
    """
    API endpoint to handle word count requests.
    Expects JSON data with a 'text' key.
    Returns JSON with 'word_count' or an 'error'.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate input data
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field in request.'}), 400 # Bad Request

        text_to_count = data['text']

        # Perform the word count using the helper function
        word_count = count_words(text_to_count)

        # Return the result as JSON
        return jsonify({'word_count': word_count})

    except Exception as e:
        # Log the exception for debugging (optional)
        app.logger.error(f"Error processing request: {e}")
        # Return a generic error message
        return jsonify({'error': 'An internal server error occurred.'}), 500 # Internal Server Error

# --- Main Execution ---

if __name__ == '__main__':
    # Run the Flask development server
    # Debug=True allows for automatic reloading on code changes and provides detailed error pages
    # In a production environment, use a proper WSGI server (like Gunicorn or uWSGI) and set debug=False
    app.run(debug=True)
