# RAG Application with FastAPI #

This project provides a set of RESTful APIs for user registration, login, ID linking, data joining across collections, and chain deletion using FastAPI and MongoDB with PyMongo.

## Features: ##
User Registration <br>
User Login<br>
Linking ID to User<br>
Joining Data from Multiple Collections<br>
Chain Delete of User Data Across Collections<br>


## Prerequisites ##

Python 3.8+<br>
MongoDB<br>
FastAPI<br>
PyMongo<br>
Uvicorn (for running the FastAPI application)<br>



Installation<br>
Clone the Repository


bash
```
    git clone https://github.com/Vaibhavg4651/FastAPi-assignment

```

### For Running the Backend ###

Create and Activate Virtual Environment

bash

```
    cd Backend
    python3 -m venv env

    For Mac/Linux
    source env/bin/activate

    For Windows
    env\Scripts\activate
    
```
### Install Dependencies ###

bash
```
    pip install -r requirements.txt
```


## Create a .env file in the root directory with the following content: ##


```
    MONGOURI=Your mongodb url
```


Start the Server


```
    uvicorn main:app --reload
    The server will be running at http://127.0.0.1:8000.
```


## Endpoints ##


GET /

Returns a simple greeting message.

`json`
```
{
  "Hello": "World"
}
```


`Add User`

POST /Register/
```

Request:
{
    "username": "vaibhav",
    "email": "vaibhav@gmail.com",
    "password": "Password"
}

Response:
{
  "user_id": "66c9bb30a85815676b85f34"
}

```

`Login`

Post /login

```
Request:

{
  "email": "vaibhav@gmail.com",
  "password": "Password"
}

Response:

{
  "message": "Login successful",
  "user_id": "66c9bb30a85815676b85f34"
}

```

`Link-ID`

POST /link-id

```
Request:

{
  "user_id":"66c8f45afba30e951b7e29d3",
  "linked_id":"your ID to be linked"
}

Response:

{
  "message": "ID linked successfully"
}
```

`Joins`

GET /user-details/{userID}

```
Response:
{
  "user_info": {
    "_id": "66c9bb30a85815676b85f3a4",
    "username": "vaibhav",
    "email": "vaibhav@gmail.com",
    "password": "$2b$12$sD9G9zPoNMmaoeYiMfMQD.dCO0WfD373dw358/8.Q709fJUOwlRPq",
    "linked_id": "cakjbbsoca"
  },
  "posts": []
}
```

`Delete User`

DELETE /delete-user/{userID}

```
Response:

{
  "message": "User and related data deleted successfully"
}
```

`Create Post`

POST /posts

```
 Request:
 {
  "user_id":"66c8f45afba30e951b7e29d3",
  "title":"Adventure",
  "content":"oihsdoiao;hfohnhuohaofhoiawheofhoiwhefoidmlkfjjw"
  
}

Response:
{
    "message": "Post created successfully"
}

```

## Notes ## 
Ensure your Mongodb database is correctly configured and accessible. <br>

## Troubleshooting ##

ModuleNotFoundError: Ensure all required libraries are installed and the virtual environment is activated.<br>
Database Connection Issues: Check your database configuration in the .env file and ensure the database is running.<br>
For further assistance, please refer to the documentation of the respective libraries or open an issue in the repository.
