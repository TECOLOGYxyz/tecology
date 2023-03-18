import time
import threading
import signal
import os
from flask import Flask

# Define a continuous task to run in the background
def continuous_task():
    while True:
        print("Running continuous task...")
        time.sleep(1)

# Define the Flask app
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

# Define a class to use with Gunicorn
class FlaskApplication:
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application

    def run(self):
        try:
            self.application.run(debug=False)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        pass

# Define a signal handler to gracefully stop the program
def signal_handler(sig, frame):
    print("Stopping Flask app and main program...")
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    # Set up signal handler to gracefully stop the program
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the continuous task in a separate thread
    task_thread = threading.Thread(target=continuous_task)
    task_thread.start()

    # Start the Flask app in a separate thread using Gunicorn
    options = {
        "bind": "0.0.0.0:8000",
        "workers": 4,
        "worker_class": "sync"
    }
    gunicorn_app = FlaskApplication(app, options=options)
    gunicorn_thread = threading.Thread(target=gunicorn_app.run)
    gunicorn_thread.start()

    # Wait for both threads to finish before exiting
    task_thread.join()
    gunicorn_thread.join()
