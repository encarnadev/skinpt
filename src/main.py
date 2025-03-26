import asyncio
import threading
from flask import Flask
from utils.skinport import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def main():
    # Iniciar Flask en un hilo separado
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Ejecutar el bot asíncrono
    asyncio.run(run_bot())

if __name__ == "__main__":
    main() 
