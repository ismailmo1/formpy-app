import os

from app import create_app

config_file = os.environ["FLASK_CONFIG_FILE"]
app = create_app(config_file)

if __name__ == "__main__":
    app.run()
