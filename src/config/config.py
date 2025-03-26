import os
import base64
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
APP_ID = 252490  # Rust's App ID
DESIRED_PROFIT_PERCENTAGE = 20  # Minimum profit percentage to consider a good deal

# Skinport Authentication
CLIENT_ID = os.getenv('SKINPORT_CLIENT_ID')
CLIENT_SECRET = os.getenv('SKINPORT_CLIENT_SECRET')

# Generate Basic Auth token
AUTH_TOKEN = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode() 
