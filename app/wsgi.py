from dotenv import dotenv_values, load_dotenv

# load env before importing app
load_dotenv()
print(dotenv_values())
from app import app as application

if __name__ == "__main__":
    application.run()
