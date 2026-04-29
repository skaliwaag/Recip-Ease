from dotenv import load_dotenv
import os

# load_dotenv must come before importing from app — create_app() reads os.environ at startup,
# so the MONGO_URI won't be set if dotenv loads after the import
# dirname(__file__) anchors the .env lookup to this file's location, not the shell's cwd
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
