# SNSU Tracker API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Interactive Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## User Endpoints

### Create User
**POST** `/users`

**Request Body:**
```json
{
  "username": "jdoe",
  "full_name": "John Doe",
  "initials": "JD",
  "team_name": "Operations"
}
```

**Response:**
```json
{
  "message": "User created",
  "data": {
    "user_id": 1
  }
}
```

### Get All Users
**GET** `/users`

**Response:**
```json
{
  "data": [
    {
      "user_id": 1,
      "username": "jdoe",
      "full_name": "John Doe",
      "initials": "JD",
      "team_name": "Operations",
      "is_active": 1,
      "created_at": "2024-01-01 12:00:00"
    }
  ]
}
```

### Get User by ID
**GET** `/users/{user_id}`

**Response:**
```json
{
  "data": {
    "user_id": 1,
    "username": "jdoe",
    "full_name": "John Doe",
    "initials": "JD",
    "team_name": "Operations",
    "is_active": 1,
    "created_at": "2024-01-01 12:00:00"
  }
}
```

### Update User
**PUT** `/users/{user_id}`

**Request Body:**
```json
{
  "full_name": "Jane Doe",
  "initials": "JD2"
}
```

**Response:**
```json
{
  "message": "User updated"
}
```

### Delete User (Hard Delete)
**DELETE** `/users/{user_id}`

**Response:**
```json
{
  "message": "User deleted"
}
```

### Deactivate User (Soft Delete)
**POST** `/users/{user_id}/deactivate`

**Response:**
```json
{
  "message": "User deactivated"
}
```

---

## Utility Endpoints

### Clear All Data
**POST** `/clear-data`

**Response:**
```json
{
  "message": "All data cleared"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "UNIQUE constraint failed: users.username"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

---

## Database Schema

### Tables
- `lines` - Individual production lines
- `process_steps` - Workflow steps
- `runs` - Startup run instances
- `step_executions` - Step completion tracking
- `checklist_templates` - Reusable checklists
- `checklist_items` - Individual checklist items
- `checklist_completions` - Checklist completion tracking
- `communication_notes` - Team communication
- `users` - System users

---

## Status Values

### step_executions.status
- `not-started`
- `in-progress`
- `completed`

### runs.status
- `active`
- `completed`
- `cancelled`

---

## Development

### Start Server
```bash
cd backend
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

### Run Tests
```bash
cd backend
python -m pytest tests/ -v
```
