from dotenv import load_dotenv

# load env before importing app
load_dotenv()
from app import app as application

if __name__ == "__main__":
    application.run()
