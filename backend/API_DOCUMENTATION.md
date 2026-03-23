# SNSU Tracker API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Interactive Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Lines

### Create Line
**POST** `/lines`

`line_id` is set equal to `line_number`. Line numbers must be unique.

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| line_number | integer | Yes | Unique line number (also used as line_id) |

**Response (200):**
```json
{
  "message": "Line created",
  "data": { "line_id": 1 }
}
```

**Response (409) — Duplicate:**
```json
{
  "detail": "Line 1 already exists"
}
```

---

### Get All Lines
**GET** `/lines`

Returns lines ordered by `display_order`.

**Response (200):**
```json
{
  "data": [
    {
      "line_id": 1,
      "line_number": 1,
      "display_order": 1,
      "created_at": "2026-03-23 19:53:30"
    }
  ]
}
```

---

### Get Line by ID
**GET** `/lines/{line_id}`

**Response (200):**
```json
{
  "data": {
    "line_id": 1,
    "line_number": 1,
    "display_order": 1,
    "created_at": "2026-03-23 19:53:30"
  }
}
```

---

### Update Line
**PUT** `/lines/{line_id}`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| line_number | integer | No | New line number |

**Response (200):**
```json
{
  "message": "Line updated"
}
```

---

### Delete Line
**DELETE** `/lines/{line_id}`

**Response (200):**
```json
{
  "message": "Line deleted"
}
```

---

### Reorder Lines
**PUT** `/lines/reorder`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ordered_ids | integer[] | Yes | Line IDs in desired display order |

**Response (200):**
```json
{
  "message": "Lines reordered"
}
```

---

## Process Steps

### Create Step
**POST** `/process-steps`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| step_order | integer | Yes | Position in workflow |
| team_name | string | Yes | Team/owner name |
| task_name | string | Yes | Task description |
| avg_duration_minutes | integer | No | Expected duration |

**Response (200):**
```json
{
  "message": "Step created",
  "data": { "step_id": 1 }
}
```

---

### Get All Steps
**GET** `/process-steps`

Returns steps ordered by `step_order`.

**Response (200):**
```json
{
  "data": [
    {
      "step_id": 1,
      "step_order": 1,
      "team_name": "Ops",
      "task_name": "Shutdown",
      "avg_duration_minutes": null
    }
  ]
}
```

---

### Get Step by ID
**GET** `/process-steps/{step_id}`

**Response (200):**
```json
{
  "data": {
    "step_id": 1,
    "step_order": 1,
    "team_name": "Ops",
    "task_name": "Shutdown",
    "avg_duration_minutes": null
  }
}
```

---

### Update Step
**PUT** `/process-steps/{step_id}`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| step_order | integer | No | Position in workflow |
| team_name | string | No | Team/owner name |
| task_name | string | No | Task description |
| avg_duration_minutes | integer | No | Expected duration |

**Response (200):**
```json
{
  "message": "Step updated"
}
```

---

### Delete Step
**DELETE** `/process-steps/{step_id}`

**Response (200):**
```json
{
  "message": "Step deleted"
}
```

---

### Reorder Steps
**PUT** `/process-steps/reorder`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ordered_ids | integer[] | Yes | Step IDs in desired order |

**Response (200):**
```json
{
  "message": "Steps reordered"
}
```

---

## Runs

### Create Run
**POST** `/runs`

If `work_order_end_time` or `target_ready_time` are omitted, random demo values are generated.

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| line_id | integer | Yes | Associated line ID |
| status | string | Yes | Run status |
| work_order_end_time | string | No | ISO 8601 timestamp |
| target_ready_time | string | No | ISO 8601 timestamp |

**Response (200):**
```json
{
  "message": "Run created",
  "data": {
    "run_id": 1,
    "line_id": 1,
    "work_order_end_time": "2026-03-20T17:50:00",
    "target_ready_time": "2026-03-23T09:48:00",
    "actual_ready_time": null,
    "total_duration_minutes": null,
    "status": "in_progress",
    "created_at": "2026-03-23 19:51:28"
  }
}
```

---

### Get All Runs
**GET** `/runs`

Returns runs ordered by `created_at` descending.

**Response (200):**
```json
{
  "data": [ ... ]
}
```

---

### Get Active Runs
**GET** `/runs/active`

Returns runs where `status = 'active'`.

**Response (200):**
```json
{
  "data": [ ... ]
}
```

---

### Get Run by ID
**GET** `/runs/{run_id}`

**Response (200):**
```json
{
  "data": {
    "run_id": 1,
    "line_id": 1,
    "work_order_end_time": "2026-03-20T17:50:00",
    "target_ready_time": "2026-03-23T09:48:00",
    "actual_ready_time": null,
    "total_duration_minutes": null,
    "status": "in_progress",
    "created_at": "2026-03-23 19:51:28"
  }
}
```

---

### Update Run
**PUT** `/runs/{run_id}`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| actual_ready_time | string | No | ISO 8601 timestamp |
| total_duration_minutes | integer | No | Total run duration |
| status | string | No | Run status |

**Response (200):**
```json
{
  "message": "Run updated"
}
```

---

### Delete Run
**DELETE** `/runs/{run_id}`

**Response (200):**
```json
{
  "message": "Run deleted"
}
```

---

## Step Executions

### Create Execution
**POST** `/step-executions`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| run_id | integer | Yes | Associated run ID |
| step_id | integer | Yes | Associated step ID |
| status | string | Yes | Execution status |

**Response (200):**
```json
{
  "message": "Execution created",
  "data": { "execution_id": 1 }
}
```

---

### Get Executions by Run
**GET** `/step-executions/run/{run_id}`

**Response (200):**
```json
{
  "data": [
    {
      "execution_id": 1,
      "run_id": 1,
      "step_id": 1,
      "status": "in_progress",
      "start_time": null,
      "end_time": null,
      "duration_minutes": null,
      "signed_by": null,
      "signed_at": null
    }
  ]
}
```

---

### Get Execution by ID
**GET** `/step-executions/{execution_id}`

**Response (200):**
```json
{
  "data": {
    "execution_id": 1,
    "run_id": 1,
    "step_id": 1,
    "status": "completed",
    "start_time": "2026-03-20T17:50:00",
    "end_time": "2026-03-20T18:30:00",
    "duration_minutes": 40,
    "signed_by": "JD",
    "signed_at": "2026-03-23T20:00:00"
  }
}
```

---

### Update Execution
**PUT** `/step-executions/{execution_id}`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | No | Execution status |
| start_time | string | No | ISO 8601 timestamp |
| end_time | string | No | ISO 8601 timestamp |
| duration_minutes | integer | No | Calculated duration |
| signed_by | string | No | Initials of signer |
| signed_at | string | No | ISO 8601 sign-off timestamp |

**Response (200):**
```json
{
  "message": "Execution updated"
}
```

---

### Delete Execution
**DELETE** `/step-executions/{execution_id}`

**Response (200):**
```json
{
  "message": "Execution deleted"
}
```

---

## Utility Endpoints

### Clear All Data
**POST** `/clear-data`

Drops and recreates all tables.

**Response (200):**
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

### 409 Conflict
```json
{
  "detail": "Line {number} already exists"
}
```

---

## Database Schema

### lines
| Column | Type | Constraints |
|--------|------|-------------|
| line_id | INTEGER | PRIMARY KEY (= line_number) |
| line_number | INTEGER | UNIQUE, NOT NULL |
| display_order | INTEGER | NOT NULL, DEFAULT 0 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

### process_steps
| Column | Type | Constraints |
|--------|------|-------------|
| step_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| step_order | INTEGER | NOT NULL |
| team_name | TEXT | NOT NULL |
| task_name | TEXT | NOT NULL |
| avg_duration_minutes | INTEGER | |

### runs
| Column | Type | Constraints |
|--------|------|-------------|
| run_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| line_id | INTEGER | NOT NULL, FK → lines(line_id) |
| work_order_end_time | TIMESTAMP | |
| target_ready_time | TIMESTAMP | |
| actual_ready_time | TIMESTAMP | |
| total_duration_minutes | INTEGER | |
| status | TEXT | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

### step_executions
| Column | Type | Constraints |
|--------|------|-------------|
| execution_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| run_id | INTEGER | NOT NULL, FK → runs(run_id) |
| step_id | INTEGER | NOT NULL, FK → process_steps(step_id) |
| status | TEXT | NOT NULL |
| start_time | TIMESTAMP | |
| end_time | TIMESTAMP | |
| duration_minutes | INTEGER | |
| signed_by | TEXT | |
| signed_at | TIMESTAMP | |

---

## Status Values

### step_executions.status
- `in_progress`
- `completed`

### runs.status
- `in_progress`
- `active`
- `completed`
- `cancelled`
