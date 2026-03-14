from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str


class Property(BaseModel):
    id: int
    title: str
    price: float
    owner_id: int


class Review(BaseModel):
    id: int
    property_id: int
    user_id: int
    rating: int
    comment: str


users = []
properties = []
reviews = []

@app.post("/users", status_code=201)
def create_user(user: User):
    users.append(user)
    return user


@app.get("/users", response_model=List[User])
def get_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users.pop(i)
            return
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/properties", status_code=201)
def create_property(property: Property):
    properties.append(property)
    return property


@app.get("/properties")
def get_properties(
    page: int = 1,
    limit: int = 5,
    sort_by: Optional[str] = None,
    min_price: Optional[float] = None
):
    
    result = properties

    if min_price:
        result = [p for p in result if p.price >= min_price]

    if sort_by == "price":
        result = sorted(result, key=lambda x: x.price)

    start = (page - 1) * limit
    end = start + limit

    return result[start:end]


@app.get("/properties/{property_id}")
def get_property(property_id: int):
    for p in properties:
        if p.id == property_id:
            return p
    raise HTTPException(status_code=404, detail="Property not found")


@app.delete("/properties/{property_id}", status_code=204)
def delete_property(property_id: int):
    for i, p in enumerate(properties):
        if p.id == property_id:
            properties.pop(i)
            return
    raise HTTPException(status_code=404, detail="Property not found")


@app.post("/reviews", status_code=201)
def create_review(review: Review):
    reviews.append(review)
    return review


@app.get("/reviews")
def get_reviews():
    return reviews


@app.get("/properties/{property_id}/reviews")
def get_property_reviews(property_id: int):
    return [r for r in reviews if r.property_id == property_id]