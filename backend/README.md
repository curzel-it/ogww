## Scripts
Run server
```bash
uvicorn app.main:app --reload
```

Create migrations
```
alembic revision --autogenerate -m "No comment"
```

## Curls
Example Requests
Here are some example requests you can make using cURL or tools like Postman:

#### Register a New User
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
-H "Content-Type: application/json" \
-d '{
  "username": "hiddenmugs",
  "email": "saffo.montesi@gmail.com",
  "password": "notsecure"
}'
```

#### Obtain a Token
```bash
curl -X POST "http://127.0.0.1:8000/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=hiddenmugs&password=notsecure"
```

The response will contain an access_token:

```json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
```

#### Create a Hero
```bash
curl -X POST "http://127.0.0.1:8000/heroes/" \
-H "Authorization: Bearer token" \
-H "Content-Type: application/json" \
-d '{ "name": "Sakura" }'
```