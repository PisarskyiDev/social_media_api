# Social Media API

### Technologies has use:
1. Use Celery as task scheduler for random Post generated for Social Media API.
2. Python, Django ORM, Django REST framework, PostgreSQL, Git.
3. All endpoints should be documented via Swagger.

### How to run:
- Download project from github > checkout to develop branch
- `git clone https://github.com/Soobig666/social_media_api.git`
- `git checkout develop`
- Copy .env.sample -> .env and populate with all required data
- `docker-compose up --build`
- Create admin user & Create schedule for running sync in DB

### Overview

This API gives users the ability to interact with a blog. It provides several endpoints to manipulate and retrieve data about posts, their associated comments, and likes.

### Endpoints

- List of all posts
"/api/blog/posts/"

- Details of a specific post
"/api/blog/posts/{post_pk}"

- All comments of a specific post
"/api/blog/posts/{post_pk}/commentary/"

- All likes of a specific post
"/api/blog/posts/{post_pk}/like/"

- Details of a specific comment
"/api/blog/posts/{post_pk}/commentary/{id}/"

- Details of a specific like
"/api/blog/posts/{post_pk}/like/{id}/"

Replace {post_pk} with the ID of the post and {id} with the ID of the like you want to retrieve. This endpoint provides detailed information about a specific like associated with the specified post.