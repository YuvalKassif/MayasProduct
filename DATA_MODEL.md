Data Model

Overview
- Relational model in PostgreSQL with strong integrity constraints.
- Use UUID primary keys; created_at/updated_at timestamps on all tables.
- Soft deletes only when necessary (e.g., items) via deleted_at; otherwise hard delete.

Entities
- users
  - id (uuid, pk)
  - email (citext, unique)
  - email_verified (boolean)
  - password_hash (text, nullable if social login)
  - role (enum: user, moderator, admin)
  - created_at, updated_at

- profiles (1:1 users)
  - id (uuid, pk, fk users.id)
  - username (citext, unique)
  - full_name (text)
  - bio (text)
  - avatar_key (text, S3 key)
  - location_city (text)
  - location_country (text)
  - size_top (text, nullable)
  - size_bottom (text, nullable)
  - created_at, updated_at

- follows (user FOLLOWS user)
  - follower_id (uuid, fk users.id)
  - followee_id (uuid, fk users.id)
  - created_at
  - pk (follower_id, followee_id)

- items
  - id (uuid, pk)
  - seller_id (uuid, fk users.id)
  - title (text)
  - description (text)
  - category (enum: tops, bottoms, outerwear, dresses, shoes, accessories, other)
  - brand (text)
  - size (text)
  - condition (enum: new_with_tags, like_new, good, fair)
  - price_cents (int)
  - currency (char(3))
  - location_city (text)
  - location_country (text)
  - status (enum: active, reserved, sold, hidden)
  - like_count (int, default 0)
  - favorite_count (int, default 0)
  - comment_count (int, default 0)
  - created_at, updated_at, deleted_at (nullable)

- item_images
  - id (uuid, pk)
  - item_id (uuid, fk items.id)
  - original_key (text)
  - thumb_key (text)
  - medium_key (text)
  - width (int), height (int)
  - sort_order (int)
  - created_at

- likes (user likes item)
  - user_id (uuid, fk users.id)
  - item_id (uuid, fk items.id)
  - created_at
  - pk (user_id, item_id)

- favorites (user saves item)
  - user_id (uuid, fk users.id)
  - item_id (uuid, fk items.id)
  - created_at
  - pk (user_id, item_id)

- comments
  - id (uuid, pk)
  - item_id (uuid, fk items.id)
  - author_id (uuid, fk users.id)
  - body (text)
  - created_at, updated_at, deleted_at (nullable)

- notifications
  - id (uuid, pk)
  - user_id (uuid, fk users.id)
  - type (enum: new_follower, item_liked, item_commented, item_status_changed)
  - payload (jsonb)
  - is_read (boolean)
  - created_at

- reports
  - id (uuid, pk)
  - reporter_id (uuid, fk users.id)
  - target_type (enum: user, item, comment)
  - target_id (uuid)
  - reason (text)
  - status (enum: open, reviewing, actioned, dismissed)
  - created_at, updated_at

Indexes & Constraints (selected)
- users.email unique; profiles.username unique.
- items: idx on (seller_id, created_at desc); GIN FTS (title, description).
- likes/favorites unique composite keys; foreign key cascades with sensible ON DELETE (e.g., cascade likes on item delete).
- comments: idx on (item_id, created_at desc).

FTS Strategy
- Weighted tsvector on title (A) and description (B);
- Language-specific configurations; trigram index for fuzzy search optional.

Data Retention & GDPR Hooks
- deleted_at soft delete for items/comments to allow appeals.
- user deletion: cascade or anonymize PII while retaining aggregate metrics; export via on-demand job.

