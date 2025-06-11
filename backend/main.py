from fastapi import FastAPI, File, UploadFile, WebSocket,Form
from typing import Annotated,Optional
import os
from fastapi.middleware.cors import CORSMiddleware
from agent import run_ai_generated_code
import uuid
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_UPLOAD_PATH = "/datasets"
PLOTS_DIR = "Plots"

# os.makedirs(CSV_UPLOAD_PATH, exist_ok=True)
# os.makedirs(PLOTS_DIR, exist_ok=True)

app.mount("/Plots", StaticFiles(directory=PLOTS_DIR), name="plots")
ws_clients = {}

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    try:
        await websocket.send_text("Starting analysis...")
        await websocket.send_text("Generating code from Gemini...")
        await websocket.send_text("Running code in sandbox...")
        await websocket.send_text("Saving generated plots...")
        await websocket.send_text("Analysis complete.")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")

def clear_plots():
    folders_to_clear = ['Plots', 'datasets']
    for folder in folders_to_clear:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
                
@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), plot_type: Optional[str] = Form(None)):
    clear_plots()
    task_id = str(uuid.uuid4())
    file_location = f"datasets/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    #plot_types_list = json.loads(plot_type)
    result = run_ai_generated_code(file_location, plot_type=plot_type)
    return {
        "task_id": task_id,
        "stdout": result["stdout"],
        "images": result["plots"],
    }

