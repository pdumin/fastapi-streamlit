import PIL
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from utils.model_func import class_id_to_label, load_model, transform_image

model = None 
app = FastAPI()


# Create class of answer: only class name 
class ImageClass(BaseModel):
    prediction: str

class TextClass(BaseModel):
    text: str

# Load model at startup
@app.on_event("startup")
def startup_event():
    global model
    model = load_model()

@app.get('/')
def return_info():
    return 'Hello FastAPI'


@app.post('/classify')
def classify(file: UploadFile = File(...)):
    image = PIL.Image.open(file.file)
    adapted_image = transform_image(image)
    pred_index = model(adapted_image.unsqueeze(0)).detach().cpu().numpy().argmax()
    imagenet_class = class_id_to_label(pred_index)
    response = ImageClass(
        prediction=imagenet_class
    )
    return response

@app.post('/clf_text')
def clf_text(data: TextClass):
    print(data.text)
    return data



##### run from api folder:
##### uvicorn app.main:app