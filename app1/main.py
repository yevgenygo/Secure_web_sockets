from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import websockets
import ssl
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root_func():
    return "<p>Welcome to App1</p>"

@app.get("/test_app2", response_class=HTMLResponse)
async def websocket_test_app2():
    # WebSocket URL of App2
    app2_url = "wss://app2:3001/ws" #access contaner on the same docker compose

    #local_ip = os.getenv('LOCAL_IP', '192.168.14.159')# IP of the local host
    #app2_url = f"wss://{local_ip}:3001/ws" # this is not the best solution


    #Create an SSL context
    try:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_verify_locations('server.crt')
    except ssl.SSLError as ssl_error:
        app2_status = f"Failed to create SSL context or load certificate: {str(ssl_error)}"
        return create_responce(app2_status)
    except FileNotFoundError as fnf_error:
        app2_status = f"Certificate file not found: {str(fnf_error)}"
        return create_responce(app2_status)
    except Exception as e:
        app2_status = f"An unexpected error occurred: {str(e)}"
        return create_responce(app2_status)

    try:
        # Test the secured websocket connection with app2
        async with websockets.connect(app2_url, ssl=ssl_context) as websocket:
            await websocket.send("Hello from App1!")
            response = await websocket.recv()
            app2_status = f"<p>Connection established</p>"
    except Exception as e:
        app2_status = f"Failed to establish a secure WebSocket connection: {str(e)}"
        return create_responce(app2_status)
    # Return an HTML page in case no exception was thrown
    return create_responce(app2_status)

# Create HTML for response for the client
def create_responce(app2_status):
    return f"""
    <html>
        <head>
            <title>WebSocket Security Check with App2</title>
        </head>
        <body>
            <h1>App1</h1>
            <p>Attempting to connect to the secure WebSocket in App2...</p>
            <p>Status: {app2_status}</p>
        </body>
    </html>
    """
