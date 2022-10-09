from os import access
import uvicorn
from uvicorn.config import LOGGING_CONFIG

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True, access_log=False)
