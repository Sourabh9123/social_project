## social_project

### Overview

This project is a web application built with Django and PostgreSQL, managed using Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Setup

### 1. Clone the Repository

```
git clone https://github.com/Sourabh9123/social_project.git
cd social_project
```

## 2. build and run container
```
docker-compose up --build -d
```



##### if you are runnig first time this project you have to execute these commands too ortherwise ignore it

```
docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate


```

### Create a Superuser

```
docker-compose exec web python manage.py createsuperuser
```

### i have added a postman collection too in the project directory name of the file is --->> socialpostman_collection.json

### here is some information about apis too





### User Registration
```
http://127.0.0.1:8000/api/account/signup/


request type Post

paylod = {
    "email" :"sourabh081@gmail.com",
    "password" : 9038,
    "first_name" :"sourabh",
    "last_name" :"das"
}

response = {
    "token": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cXJfaWQiOjEyfQ.UI6dXvBEh-NEl_iwnox0Eu-gmJL3__SbiufRGSUUQ9E",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlb6MTJ9.SdP7aIrhfsF0ja30A90gxo1lkiGrDVcuprVcICJlQ1E"
    }
}


use access token for authentication

```
### use access token for authentication

### user login
```
http://127.0.0.1:8000/api/account/login/

request Type = Post

payload = {
    "email" :"sourabh081@gmail.com",
    "password" : 9038s
   
}

response = {
    "token": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cXJfaWQiOjEyfQ.UI6dXvBEh-NEl_iwnox0Eu-gmJL3__SbiufRGSUUQ9E",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlb6MTJ9.SdP7aIrhfsF0ja30A90gxo1lkiGrDVcuprVcICJlQ1E"
    }
}

```


### Search Users


```
http://127.0.0.1:8000/api/search/?query=<your_serach_key>

Example : You want to search sourabh


http://127.0.0.1:8000/api/search/?query=sourabh

Request Type = Get

Headers:
    Authorization: Bearer Token
    Content-Type: application/json




response = {
     "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "first_name": "sourabh ",
            "last_name": "das"
        },
        {
            "id": 2,
            "first_name": "False",
            "last_name": "False"
        },
        {
            "id": 6,
            "first_name": "False",
            "last_name": "False"
        },
        {
            "id": 7,
            "first_name": "False",
            "last_name": "False"
        },
    
    ]
}

```


### Send Friend Request

you can get the user id by searching his name or email  on the above request  http://127.0.0.1:8000/api/search/?query=sourabh

```
http://127.0.0.1:8000/api/send-friend-req/

Example: You want to send request to a person whose id is 1

http://127.0.0.1:8000/api/send-friend-req/

Headers:
    Authorization: Bearer Token
    Content-Type: application/json


Request Type = Post
payload = {
    "user_id":1
}

response = {
message": "Friendship request sent successfully."
}

```



## View Friend Request


```
http://127.0.0.1:8000/api/view-friend-req/

Headers:
    Authorization: Bearer Token
    Content-Type: application/json

request Type : Get
response = {
    "friend_requests": [
        {
            "sender": {
                "id": 12,
                "first_name": "sourabh",
                "last_name": "das"
            },
            "status": "pending",
            "created_at": "2024-06-14T07:05:12.025128Z"
        }
    ]

}
```



### Accept Friend Request

```
http://127.0.0.1:8000/api/accept-req/

Example: you want to accept request of a person whose id is 1

http://127.0.0.1:8000/api/accept-req/

Request Type : Post


Headers:
    Authorization: Bearer Token
    Content-Type: application/json

payload = {
    "user_id":1
}


response = {
    "Request Accepted", status=status.HTTP_200_OK
}

```



### Reject Friend Request 

```
http://127.0.0.1:8000/api/reject-req/

The whose friend request you want to reject is id 1

Example : http://127.0.0.1:8000/api/reject-req/


Request Type = Post


Headers:
    Authorization: Bearer Token
    Content-Type: application/json

payload = {
    "user_id":1
}

response = {
    "Request Rejected", status=status.HTTP_200_OK
}

```

### List Your All Friends


```
http://127.0.0.1:8000/api/friends/

Request Type = Get
Headers:
    Authorization: Bearer Token
    Content-Type: application/json


response = {
     "my_friends": [
        {
            "unique_id": 2,
            "email": "billy67@example.org",
            "first_name": "False",
            "last_name": "False"
        },
        {
            "unique_id": 4,
            "email": "david27@example.org",
            "first_name": "False",
            "last_name": "False"
        }
    ]
}

```



