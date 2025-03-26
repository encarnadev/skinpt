import time
import threading
from flask import Flask
from utils.skinport import sio

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def run_bot():
    while True:
        try:
            sio.connect('wss://skinport.com')
            sio.wait()
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(5)  # Wait 5 seconds before reconnecting

def main():
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run the bot in the main thread
    run_bot()

if __name__ == "__main__":
    main() 
