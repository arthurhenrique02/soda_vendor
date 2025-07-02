from fastapi import FastAPI
from core.config import configure_cors, configure_routes, configure_db

def create_app() -> FastAPI:
    app = FastAPI(title="Soda Vendor API", version="1.0.0")
    
    configure_cors(app)
    configure_routes(app)
    configure_db()
    
    return app


app = create_app()