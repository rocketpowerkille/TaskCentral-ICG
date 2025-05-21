# Import the Flask application instance from our app.py module
from app import app


if __name__ == "__main__":
    # Start the Flask development server
    
    app.run(host="0.0.0.0", port=5000, debug=True)
