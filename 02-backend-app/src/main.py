from fastapi import FastAPI

# 1. Create the application instance
app = FastAPI()

# 2. Define a "Path Operation" (a route)
@app.get("/")
async def read_root():
    """
    Handles GET requests to the root URL (/).
    Returns a simple JSON message.
    """
    return {"message": "Hello from your k8s cluster!"}

# Health Check Endpoint for Kubernetes Probes
@app.get("/healthz")
async def health_check():
    """
    Returns 200 OK to tell Kubernetes the container is healthy.
    """
    return {"status": "ok"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    """
    Handles GET requests with a path parameter (item_id)
    and an optional query parameter (q).
    """
    return {"item_id": item_id, "query": q}