import os
import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from dotenv import load_dotenv

# 1. Load the environment variables from the .env file
load_dotenv()

app = FastAPI(title="Agentic POS Middleware")

# 2. Fetch the topic securely. If it fails, it uses a fallback.
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "default_fallback_topic")
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

async def send_push_notification(title: str, message: str, priority: str = "default"):
    """
    This is the Agent's Effector. It interacts with the outside world.
    Because it's 'async', it yields control back to the event loop while waiting for the network.
    """
    headers = {
        "Title": title,
        "Priority": priority,
        "Tags": "robot,rotating_light"  # Adds cool icons to your phone notification
    }
    
    # We use 'async with' to properly open and close the network connection
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                NTFY_URL,
                data=message.encode('utf-8'),
                headers=headers
            )
            print(f"[AGENT LOG] Success! External voice routed to topic: {NTFY_TOPIC}")
        except Exception as e:
            print(f"[AGENT ERROR] Network failure reaching ntfy.sh: {e}")

@app.post("/api/v1/agent/webhook")
async def handle_odoo_signal(request: Request, background_tasks: BackgroundTasks):
    """
    This endpoint receives the 'Handshake' from Odoo.
    """
    # Step A: Parse the incoming JSON payload from Odoo
    payload = await request.json()
    
    # Step B: Extract the Agent's Beliefs and Intentions
    product_name = payload.get("product_name", "Unknown Product")
    stock_level = payload.get("stock_level", 0)
    agent_intent = payload.get("intent", "Manual review required")
    priority_level = payload.get("agent_stock_priority", "default")
    
    # Map Odoo's priority to ntfy's priority scale
    ntfy_priority = "high" if priority_level == "critical" else "default"
    
    # Step C: Format the human-readable message
    title = f"Agentic Alert: {product_name}"
    message = f"Stock level at {stock_level} units. Agent Intention: {agent_intent}"
    
    # Step D: The Magic Trick (Background Tasks)
    # We tell FastAPI: "Hey, run this function in the background, don't wait for it."
    background_tasks.add_task(send_push_notification, title, message, ntfy_priority)
    
    # Step E: Instant Response
    # We return a 200 OK to Odoo immediately. This prevents Thread Blocking in the POS!
    return {"status": "success", "message": "Signal received. Processing in background."}