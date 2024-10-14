# Install dependencies from requirements.txt
install:
	pip install -r requirements.txt

# Detect the OS and use appropriate commands
ifeq ($(OS),Windows_NT)
    # Commands for Windows
    run:
	    set FLASK_APP=app.py && set FLASK_RUN_PORT=3000 && flask run --host=0.0.0.0 --port=3000
else
    # Commands for macOS/Linux (Unix-based systems)
    run:
	    FLASK_APP=app.py FLASK_RUN_PORT=3000 flask run --host=0.0.0.0 --port=3000
endif
