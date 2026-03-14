from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os

app = FastAPI(title="Real Estate API with Images")

# CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users = []
properties = []
reviews = []

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class Property(BaseModel):
    id: Optional[int] = None
    title: str
    price: float
    description: Optional[str] = ""
    location: Optional[str] = ""
    type: Optional[str] = "Apartment"
    owner_id: int
    image_url: Optional[str] = None  # нове поле для фото

class Review(BaseModel):
    id: Optional[int] = None
    property_id: int
    user_id: int
    rating: int
    comment: str

# =====================
# USERS
# =====================
@app.post("/register", status_code=201)
def register_user(user: User):
    for u in users:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    user.id = len(users) + 1
    users.append(user)
    return {"message": "User registered", "user_id": user.id}

@app.post("/login")
def login_user(login_req: LoginRequest):
    for user in users:
        if user.email == login_req.email and user.password == login_req.password:
            return {"token": f"fake-token-for-{user.id}"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# =====================
# PROPERTIES
# =====================
@app.post("/properties", status_code=201)
async def create_property(
    title: str = Form(...),
    price: float = Form(...),
    description: str = Form(""),
    location: str = Form(""),
    type: str = Form("Apartment"),
    owner_id: int = Form(...),
    image: UploadFile = File(None)
):
    prop_id = len(properties) + 1
    image_url = None

    # Зберігаємо фото, якщо воно є
    if image:
        filename = f"{prop_id}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/images/{filename}"

    prop = Property(
        id=prop_id,
        title=title,
        price=price,
        description=description,
        location=location,
        type=type,
        owner_id=owner_id,
        image_url=image_url
    )
    properties.append(prop)
    return prop

@app.get("/properties")
def get_properties():
    return properties

@app.get("/properties/{property_id}")
def get_property(property_id: int):
    for p in properties:
        if p.id == property_id:
            return p
    raise HTTPException(status_code=404, detail="Property not found")

# =====================
# IMAGE SERVING
# =====================
@app.get("/images/{filename}")
def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

# =====================
# REVIEWS
# =====================
@app.post("/reviews", status_code=201)
def create_review(review: Review):
    review.id = len(reviews) + 1
    reviews.append(review)
    return review

@app.get("/reviews")
def get_reviews():
    return reviews

@app.get("/properties/{property_id}/reviews")
def get_property_reviews(property_id: int):
    return [r for r in reviews if r.property_id == property_id]