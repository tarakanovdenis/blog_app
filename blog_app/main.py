import uvicorn

from src.core.config import log_config


if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_config=log_config,
        reload=True,
    )
