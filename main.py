from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from passlib.context import CryptContext
from bson.objectid import ObjectId
from model import User, Login, LinkID, Post
from dotenv import load_dotenv
import os
from typing import List
from bson import ObjectId

def serialize_doc(doc):
    """
    Convert MongoDB document into a JSON serializable format.
    """
    if not doc:
        return None
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc


# Initialize FastAPI
app = FastAPI()

load_dotenv()

def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value

# Database setup
mongourl = get_env_variable("MONGOURI")
client = MongoClient(mongourl)
db = client["userdb"]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Utility functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(email: str):
    return db.users.find_one({"email": email})

def get_user_by_id(user_id: str):
    return db.users.find_one({"_id": ObjectId(user_id)})

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
async def register(user: User):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict['password'] = hashed_password

    result = db.users.insert_one(user_dict)
    return {"user_id": str(result.inserted_id)}

### 3. Login API

@app.post("/login")
async def login(login_data: Login):
    user = get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user['password']):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {"message": "Login successful", "user_id": str(user['_id'])}

### 4. Linking ID API

@app.post("/link-id")
async def link_id(link_data: LinkID):
    user = get_user_by_id(link_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.users.update_one(
        {"_id": ObjectId(link_data.user_id)},
        {"$set": {"linked_id": link_data.linked_id}}
    )
    return {"message": "ID linked successfully"}

### 5. Joins

@app.get("/user-details/{user_id}")
async def get_user_details(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(user)
    # Example: Join with another collection called `posts`
    posts = db.posts.find({"user_id": ObjectId(user_id)})
    print(posts)
    if not posts:
        posts = []
    user_details = {
        "user_info": serialize_doc(user),
        "posts": list(posts)
    }
    print(user_details)
    return user_details

### 6. Chain Delete

@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete all posts related to the user
    db.posts.delete_many({"user_id": ObjectId(user_id)})
    
    # Delete the user
    db.users.delete_one({"_id": ObjectId(user_id)})
    
    return {"message": "User and related data deleted successfully"}


# Create a new post
@app.post("/posts/", response_model=dict)
async def create_post(post: Post):
    user = get_user_by_id(post.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    post_dict = post.dict()
    post_dict['user_id'] = ObjectId(post.user_id)
    
    result = db.posts.insert_one(post_dict)
    return {"post_id": str(result.inserted_id)}

# Get all posts by a user
@app.get("/users/{user_id}/posts/", response_model=List[dict])
async def get_posts_by_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    posts = db.posts.find({"user_id": ObjectId(user_id)})
    return [serialize_doc(post) for post in posts]

# Get a single post by post ID
@app.get("/posts/{post_id}", response_model=dict)
async def get_post(post_id: str):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return serialize_doc(post)

# Update a post
@app.put("/posts/{post_id}", response_model=dict)
async def update_post(post_id: str, post_data: Post):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {
            "title": post_data.title,
            "content": post_data.content
        }}
    )
    return {"message": "Post updated successfully"}

# Delete a post
@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.posts.delete_one({"_id": ObjectId(post_id)})
    return {"message": "Post deleted successfully"}

# Running the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
