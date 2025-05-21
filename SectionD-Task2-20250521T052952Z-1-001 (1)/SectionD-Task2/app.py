import os
import logging
import uuid
import tempfile
from datetime import timedelta
from flask import Flask
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
from flask_session import Session  # Required for filesystem session

# Configure logging - This helps us debug issues by printing messages to the console
logging.basicConfig(level=logging.DEBUG)

# Create Flask app - This is the main application object that handles all requests
# Flask follows the WSGI standard and provides routing, templating, and other features
app = Flask(__name__)

# Add builtin functions to Jinja environment - This makes Python's min and max functions available in templates
# These functions help when comparing values directly in the HTML templates
app.jinja_env.globals.update(min=min)
app.jinja_env.globals.update(max=max)

# Add custom filters - These extend Jinja's template capabilities with our own functions

# This filter converts newlines to HTML breaks, useful for displaying multi-line text in HTML
@app.template_filter('nl2br')
def nl2br_filter(s):
    if s:
        # Markup ensures the HTML isn't escaped and renders properly in the browser
        return Markup(s.replace('\n', '<br>'))

# This filter formats datetime objects in a consistent way throughout the application
@app.template_filter('format_datetime')
def format_datetime_filter(dt):
    if dt:
        # Format: YYYY-MM-DD HH:MM:SS
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return ''

# Set a fixed secret key for development - In production, this would be a proper secret environment variable
# The secret key is used for securely signing session cookies and other security-related needs
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key_for_testing_purposes")

# Configure session settings for filesystem sessions - This is better than browser cookies for larger amounts of data
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions as files instead of cookies
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')  # Session storage location
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)  # Create the session directory if it doesn't exist
app.config['SESSION_PERMANENT'] = True  # Sessions persist even after browser is closed
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Sessions expire after 1 day for security
app.config['SESSION_USE_SIGNER'] = True  # Cryptographically sign session cookies for extra security
app.config['SESSION_FILE_THRESHOLD'] = 100  # Maximum number of sessions stored - Prevents disk space issues
app.config['SESSION_FILE_MODE'] = 384  # 0600 in octal - More secure session files (only owner can read/write)
app.config['SESSION_KEY_PREFIX'] = 'taskscentral:'  # Prefix for session keys - Namespaces sessions for this app
app.config['PREFERRED_URL_SCHEME'] = 'http'  # For session cookie security

# Initialize the session extension - Starts the session handling system
Session(app)

# Initialize CSRF protection - This prevents cross-site request forgery attacks
# CSRF attacks trick users into submitting requests they didn't intend to make
csrf = CSRFProtect(app)

# Import routes after app is initialized to avoid circular imports
# This pattern prevents errors where app isn't defined when routes try to use it
from routes import *

# Initialize database (in-memory for MVP)
# For this version we're using a simple in-memory database rather than a full DBMS
# This makes the app easy to run without external dependencies
from database import init_db
init_db()  # Populate with initial data
