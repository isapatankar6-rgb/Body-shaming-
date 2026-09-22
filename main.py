from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import Response
from PIL import Image
import io

app = FastAPI(title="AI Virtual Try-On API")

@app.get("/")
def root():
    return {"status": "Virtual Try-On API is running."}

@app.post("/api/v1/try-on")
async def process_try_on(
    person_image: UploadFile = File(...),
    garment_image: UploadFile = File(...),
    category: str = Form("upperbody") # upperbody, lowerbody, or dress
):
    try:
        # Read uploaded image bytes
        person_bytes = await person_image.read()
        garment_bytes = await garment_image.read()

        person_img = Image.open(io.BytesIO(person_bytes)).convert("RGB")
        garment_img = Image.open(io.BytesIO(garment_bytes)).convert("RGB")

        # --- INFERENCE STEP ---
        # Replace this placeholder block with model calls (e.g., OOTDiffusion or IDM-VTON)
        # For prototype demonstration, we return the uploaded garment image format
        output_img = garment_img.resize(person_img.size)

        # Buffer image for HTTP response
        img_byte_arr = io.BytesIO()
        output_img.save(img_byte_arr, format='JPEG')
        
        return Response(content=img_byte_arr.getvalue(), media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
