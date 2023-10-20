from os import path
from dotenv import load_dotenv
from pathlib import Path

def load_creds():
    ENV_FILE_PATH = '/root/.creds/.env'

    if not path.exists(ENV_FILE_PATH):
        ENV_FILE_PATH = input("Please enter the absolute path to your .env file on your local file system.")

    dotenv_path = Path(ENV_FILE_PATH)
    load_dotenv(dotenv_path=dotenv_path)