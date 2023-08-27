
import json
import logging
import psycopg2
from constants import NotificationCategory,NotificationTitle
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
import config

app = FastAPI()

conn = psycopg2.connect(
                    host = config.getenv("POSTGRES_HOST"),
                    dbname = config.getenv("POSTGRES_DATABASE"),
                    user = config.getenv("POSTGRES_USER"),
                    password = config.getenv("POSTGRES_PASSWORD"),
                    port = config.getenv("POSTGRES_PORT")
                )
manager = ConnectionManager()

@app.get("/health")
def get_health():
    return {"success": True}

@app.websocket("/trigger_event")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message={}
            try:
                data=json.loads(data)
            except Exception as e:
                await manager.broadcast(websocket,f"Paylaod must be json with fiels:(title,category,description (not required for message category)):{str(e)}")
                return
            if data.get("category") in [NotificationCategory.PROFILE_SETUP.value,NotificationCategory.SUBSCRIPTION_EXPIRY.value,NotificationCategory.MESSAGE.value]:
                category=data["category"]
                if category in [NotificationCategory.MESSAGE.value,NotificationCategory.SUBSCRIPTION_EXPIRY.value] and not data.get("description"):
                    await manager.broadcast(websocket,f"Description cannot be null for {data.get('category')}")
                else:
                    message["title"]=NotificationTitle.PROFILE_SETUP_COMPLETE.value if category==NotificationCategory.PROFILE_SETUP.value else NotificationTitle.SUBSCRIPTION_EXPIRING_SOON.value if category==NotificationCategory.SUBSCRIPTION_EXPIRY.value else NotificationTitle.NEW_MESSAGE_RECEIVED.value
                    message["category"]=category
                    message["description"]=data.get("description","") if category in [NotificationCategory.MESSAGE.value,NotificationCategory.SUBSCRIPTION_EXPIRY.value] else "Congratulations !!!"
                await manager.broadcast(websocket,json.dumps(message))
                cursor = conn.cursor()
                cursor.execute("INSERT INTO notifications (notification,created_on) VALUES(%s, %s)", (json.dumps(message), 'now()'))
                conn.commit()
                cursor.close()
            else:
                await manager.broadcast(websocket,f"Invalid Category")
    except WebSocketDisconnect as e:
        logging.error(f"Failed ro broadcast notification:{str(e)}")
        await manager.broadcast(websocket,f"Unexpected disconnect:{str(e)}")
        manager.disconnect()
        


@app.get("/fetch_notifications")
def fetch_notifications():
    result=[]
    try:
        cursor = conn.cursor()
        cursor.execute("select notification,created_on from notifications;")
        result = cursor.fetchall()
    except Exception as e:
        logging.error(f"Failed to fetch notifications:{str(e)}")
    return result
