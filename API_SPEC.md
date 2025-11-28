API Spec (v1)

Conventions
- Base URL: /api/v1
- Auth: Bearer in HTTP‑only cookies (access/refresh) or Authorization header.
- Pagination: cursor-based with `limit`, `cursor` returning `next_cursor`.
- Timestamps: ISO 8601 UTC.

Auth
- POST /auth/register {email, password}
- POST /auth/login {email, password}
- POST /auth/refresh (uses refresh cookie)
- POST /auth/logout
- POST /auth/password/forgot {email}
- POST /auth/password/reset {token, new_password}

Users & Profiles
- GET /users/{id}
- GET /me (current user)
- PATCH /me {profile fields}
- GET /users/{id}/followers
- GET /users/{id}/following
- POST /users/{id}/follow
- DELETE /users/{id}/follow

Items
- POST /items {title, description, category, brand, size, condition, price_cents, currency, location_* , images: [client keys]}
  - For images: client first requests presigned URLs → uploads → submits item with keys
- GET /items/{id}
- PATCH /items/{id}
- DELETE /items/{id}
- GET /users/{id}/items?status=&cursor=&limit=

Feed & Search
- GET /feed?cursor=&limit=
- GET /search?query=&category=&brand=&size=&price_min=&price_max=&condition=&location=&radius_km=&cursor=&limit=

Social
- POST /items/{id}/like
- DELETE /items/{id}/like
- POST /items/{id}/favorite
- DELETE /items/{id}/favorite

Comments
- GET /items/{id}/comments?cursor=&limit=
- POST /items/{id}/comments {body}
- PATCH /comments/{id} {body}
- DELETE /comments/{id}

Notifications
- GET /notifications?is_read=&cursor=&limit=
- POST /notifications/{id}/read

Reports
- POST /reports {target_type, target_id, reason}
- GET /admin/reports (admin)
- PATCH /admin/reports/{id} {status}

Presigned Uploads
- POST /uploads/presign {content_type, size_bytes, kind=item_image}
  → { upload_url, key, headers }

Response Envelope (example)
{ data: {...}, meta: { next_cursor }, error: null }
Or on error: { data: null, error: { code, message, details } }

Examples
- GET /feed → { data: { items: [ {id, title, price_cents, images: [...]} ] }, meta: { next_cursor } }
- POST /items → returns created item with image variants as available.

