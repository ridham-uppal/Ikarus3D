# # ---
# # File: backend/app/config.py
# # ---
# # Description: Handles configuration management, like loading environment variables.
# # It's good practice to keep secrets and configurations out of the main code.
# # ---

# import os
# from dotenv import load_dotenv

# # Load environment variables from a .env file if it exists.
# # This is useful for local development.
# load_dotenv()

# # --- API Keys and Settings ---
# PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "YOUR_API_KEY")

# # --- File Paths ---
# # We construct the path relative to this file's location to make it robust.
# # This assumes the 'data' directory is at the project root, one level above 'backend'.
# # Project Root -> data/intern_data_ikarus.csv
# # Project Root -> backend/app/config.py
# # So we go up two levels from config.py to get to the project root.
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
# # DATA_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "intern_data_ikarus.csv")
# DATA_FILE_PATH = "C:\\Users\\dparo\\OneDrive\\Desktop\\ikarus\\data\\intern_data_ikarus.csv"

# # So, we need to go up two levels from this file's directory to get to the project root ('ikarus').
# # CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is /backend/app
# # PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR)) # This is /ikarus
# # DATA_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "intern_data_ikarus.csv")


# ---
# File: backend/app/config.py
# ---
# Description: Manages configuration settings for the application, such as API keys and file paths.
# ---

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from a .env file
load_dotenv()

# --- Pinecone Configuration ---
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "furniture-recommendations"

# --- File Path Configuration ---
# Navigate up from the current file's directory ('app') to the 'backend' directory,
# and then up again to the project's root directory ('ikarus').
# This makes the path robust, regardless of where the script is run from.
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_FILE_PATH = PROJECT_ROOT / "data" / "intern_data_ikarus.csv"

# Ensure the data file exists
if not DATA_FILE_PATH.exists():
    raise FileNotFoundError(f"Data file not found at the expected path: {DATA_FILE_PATH}")

