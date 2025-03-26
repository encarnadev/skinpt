import skinport
import aiohttp
from datetime import datetime
from config.config import (
    WEBHOOK_URL, 
    CURRENCY, 
    APP_ID, 
    DESIRED_PROFIT_PERCENTAGE,
    CLIENT_ID,
    CLIENT_SECRET
)

# Crear cliente de Skinport
client = skinport.Client(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

@client.listen("saleFeed")
async def on_sale_feed(data):
    salefeed = skinport.SaleFeed(data=data)
    
    if salefeed.event_type == "listed":
        for sale in salefeed.sales:
            await process_sale(sale)

@client.listen("maintenanceUpdated")
async def on_maintenance_updated(data):
    print(f"Maintenance status updated: {data}")

@client.listen("steamStatusUpdated")
async def on_steam_status_updated(data):
    print(f"Steam status updated: {data}")

async def process_sale(sale):
    """Process a single sale item"""
    suggested_price = sale.suggested_price / 100  # Convert cents to euros
    sale_price = sale.sale_price / 100
    
    if suggested_price == 0:
        return
    
    discount = ((suggested_price - sale_price) / suggested_price) * 100
    
    if discount < DESIRED_PROFIT_PERCENTAGE:
        return
        
    await send_discord_notification(sale, suggested_price, sale_price, discount)

async def send_discord_notification(sale, suggested_price, sale_price, discount):
    """Send notification to Discord webhook"""
    embed = {
        "title": f"🔥 Good Deal Found: {sale.market_hash_name}",
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
        "footer": {"text": "Skinport Deal Bot"}
    }
    
    if sale.image:
        embed["thumbnail"] = {"url": f"https://community.cloudflare.steamstatic.com/economy/image/{sale.image}/256x256"}
    
    payload = {"embeds": [embed]}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=payload) as response:
                await response.text()
    except Exception as e:
        print(f"Error sending Discord notification: {e}")

async def run_bot():
    """Run the Skinport bot"""
    try:
        await client.start()
    except Exception as e:
        print(f"Error running bot: {e}")
        raise 
