# Koffie Tasks API endpoint reference

This reference is generated as an owned, synthetic portfolio example. It does
not describe a client or production system.

Base URL: `https://api.example.com/v1`

## `GET /tasks`

Lists tasks. Use the optional `status` query parameter with `queued`, `active`,
or `done`.

```http
GET /v1/tasks?status=active HTTP/1.1
Host: api.example.com
Accept: application/json
```

Successful response (`200`):

```json
{
  "items": [
    {
      "id": "task_01",
      "title": "Validate API contract",
      "status": "active",
      "createdAt": "2026-07-29T10:00:00Z"
    }
  ],
  "count": 1
}
```

## `POST /tasks`

Creates one task. New tasks begin in the `queued` state.

```http
POST /v1/tasks HTTP/1.1
Host: api.example.com
Content-Type: application/json

{"title":"Publish endpoint reference"}
```

Successful response (`201`) includes a `Location` header and the created task.
Invalid input returns `400` with the shared error schema.

## `GET /tasks/{taskId}`

Returns one task by identifier. Identifiers match `^task_[0-9]{2,}$`.

```http
GET /v1/tasks/task_01 HTTP/1.1
Host: api.example.com
Accept: application/json
```

Successful requests return `200`. Unknown identifiers return `404` with the
shared error schema.

## Shared error shape

```json
{
  "code": "not_found",
  "message": "task was not found"
}
```
