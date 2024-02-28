from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import base64
import os
import shutil
from ultralytics import YOLO

model = YOLO('.runs/detect/train/weights/best.pt')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/upload/")
async def update_file(encoded_content: List[str] = Form(...)):
    results = []

    for i, encoded_string in enumerate(encoded_content, start=1):
        try:
            temp_dir = "./temp_storage"
            os.makedirs(temp_dir, exist_ok=True)

            # Decode base64 and save as .jpg file
            image_data = base64.b64decode(encoded_string)
            image_path = os.path.join(temp_dir, f"image_{i}.jpg")
            with open(image_path, "wb") as f:
                f.write(image_data)

            # Run YOLO with the image path
            temp_results = model(image_path)

            # Convert YOLO results to JSON-serializable format
            
            number_of_elephants = f"{temp_results[0].boxes.shape[0]} Elephants"
            print(number_of_elephants)
            results.append(number_of_elephants)
            # Check if any objects are detected
            
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error": f"Error processing image: {str(e)}"})

        finally:
            # Remove the temporary directory and its contents
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error removing directory: {str(e)}")

    return results
