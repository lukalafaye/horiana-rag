import os
from dotenv import load_dotenv

# Define the root path of the project
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_absolute_path(relative_path):
    # Returns absolute path using relative path starting with from PROJECT_ROOT...
    return os.path.join(PROJECT_ROOT, relative_path)

load_dotenv("../.env")