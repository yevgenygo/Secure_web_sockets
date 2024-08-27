from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# Define a WebSocket endpoint at the URL path "/ws"
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Keep the connection open and listen for messages in an infinite loop
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        # Throw exception when the client disconnects
        await websocket.close()
