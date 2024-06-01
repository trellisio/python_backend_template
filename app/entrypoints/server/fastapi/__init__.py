from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def start_app():
    # TODO: initialize logger
    # TODO: initialize connections
    # TODO: start_server
    
    pass