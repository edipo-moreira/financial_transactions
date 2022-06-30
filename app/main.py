import uvicorn
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8081, reload=True)
