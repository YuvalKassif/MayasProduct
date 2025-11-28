Product Design — Second‑Hand Clothing Social Network

Vision
- Make buying and selling second‑hand clothing delightful, trustworthy, and fast.
- Enable discovery via a personalized feed, social connections, and rich filters.
- Emphasize sustainability and community norms with transparent profiles and safety.

Primary Users
- Sellers: individuals listing clothing items to sell.
- Buyers: individuals discovering, filtering, and purchasing items.
- Moderators/Admins: enforcing policies, handling reports, removing harmful content.

Core Value Props
- Personalized feed of relevant items from followed users, nearby locations, and taste-driven metadata (brand, style, size).
- Trust via rich profiles, ratings, verified signals, and transparent history.
- Fast listing workflow with multi‑image upload, auto‑resize, and smart defaults.

MVP Feature Set
- Authentication: email/password, magic link (optional), social OAuth (Google/Apple later).
- Profiles: avatar, bio, location, size info, follower/following counts.
- Items: create/edit/delete listings with photos, price, condition, brand, category, size, location, description, tags.
- Feed: reverse‑chronological + basic personalization; infinite scroll.
- Search & Filters: keyword, category, size, brand, price range, condition, location radius.
- Social: follow users, favorite/save items, like items.
- Comments: item-level comments (simple, linear threads).
- Notifications: basic (new follower, like, comment, item sold/updated) via in‑app.
- Reporting: report item/user/comment; admin tools minimal.

Post‑MVP (Phased)
- Offers/Negotiation: buyer can send offers; seller accepts/counters.
- Messaging: buyer-seller chat threads (WebSocket or long polling).
- Payments: platform-facilitated checkout and limited buyer protection.
- Shipping: address handling, label generation via carrier APIs.
- Advanced Personalization: collaborative filtering and content-based ranking.
- Moderation Enhancements: image/text classification for policy violations.

Non‑Functional Requirements
- Availability: 99.9% for core API; graceful degradation for non‑critical features.
- Performance: p95 API < 300ms for main flows; image processing async.
- Scalability: support 100k DAU MVP; horizontal scale path defined.
- Security: OWASP Top 10 mitigations; principled authZ and rate limits.
- Privacy: data minimization; user data export/delete; clear retention.
- Observability: structured logs, metrics, traces; alerting for SLO breaches.

Key User Flows (MVP)
- Onboarding: sign up → set profile basics → land on feed.
- Create Listing: add photos → set details → publish → appears in feed and search.
- Discover: scroll feed → filter → open item → favorite/follow → comment or contact (post‑MVP messaging).
- Purchase (Post‑MVP): offer/accept → pay → ship → rate.

Success Metrics (Examples)
- Activation: % new users who publish or favorite within 24h.
- Liquidity: time-to-first-view, time-to-first-message/offer, sell‑through rate.
- Retention: D1/D7/D30 retention by cohort.
- Supply/Discovery: # listings per seller per month; search→view CTR; feed dwell time.

