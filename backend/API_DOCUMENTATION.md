# SNSU Tracker API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Interactive Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

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
  "detail": "Error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
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
