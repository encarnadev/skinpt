import socketio
import requests
from datetime import datetime
from config.config import WEBHOOK_URL, CURRENCY, APP_ID, DESIRED_PROFIT_PERCENTAGE

sio = socketio.Client(transport='websocket')

def send_discord_notification(item):
    """Send notification to Discord webhook"""
    suggested_price = item.get('suggestedPrice', 0) / 100  # Convert cents to euros
    sale_price = item.get('salePrice', 0) / 100
    
    if suggested_price == 0:
        return
    
    discount = ((suggested_price - sale_price) / suggested_price) * 100
    
    if discount < DESIRED_PROFIT_PERCENTAGE:
        return
        
    embed = {
        "title": f"🔥 Good Deal Found: {item['marketName']}",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "Sale Price",
                "value": f"€{sale_price:.2f}",
                "inline": True
            },
            {
                "name": "Suggested Price",
                "value": f"€{suggested_price:.2f}",
                "inline": True
            },
            {
                "name": "Discount",
                "value": f"{discount:.2f}%",
                "inline": True
            }
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "Skinport Deal Bot"
        }
    }
    
    if item.get('image'):
        embed["thumbnail"] = {"url": f"https://community.cloudflare.steamstatic.com/economy/image/{item['image']}/256x256"}
    
    payload = {
        "embeds": [embed]
    }
    
    requests.post(WEBHOOK_URL, json=payload)

@sio.event
def connect():
    print('Connected to Skinport WebSocket')
    sio.emit('saleFeedJoin', {'currency': CURRENCY, 'locale': 'en', 'appid': APP_ID})

@sio.event
def disconnect():
    print('Disconnected from Skinport WebSocket')

@sio.event
def saleFeed(data):
    if data['eventType'] == 'listed':
        for item in data['sales']:
            send_discord_notification(item) 
