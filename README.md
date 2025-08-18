# FastAPI Social Media API

A REST API built with FastAPI for a social media platform featuring user authentication, post management, and voting functionality.

## Features

- **User Management**: User registration and authentication with JWT tokens
- **Post Management**: Create, read, update, and delete posts with ownership validation
- **Voting System**: Users can vote on posts with vote counting
- **Database Migrations**: Alembic integration for database schema management
- **Testing Suite**: Comprehensive test coverage with pytest
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing and deployment

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens) with OAuth2
- **Password Hashing**: Bcrypt
- **Database Migrations**: Alembic
- **Testing**: Pytest
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## API Endpoints

### Authentication
- `POST /login` - User login and token generation

### Users
- `POST /users/` - Create new user account
- `GET /users/{id}` - Get user details by ID

### Posts
- `GET /posts/all` - Get all posts with pagination and search
- `GET /posts/{id}` - Get specific post by ID
- `POST /posts/` - Create new post (authenticated)
- `PUT /posts/{id}` - Update post (owner only)
- `DELETE /posts/{id}` - Delete post (owner only)

### Votes
- `POST /votes/` - Vote on a post (1 for upvote, 0 to remove vote)

## Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `password` (Hashed)
- `created_at`
- `phone_number` (Optional)

### Posts Table
- `id` (Primary Key)
- `title`
- `content`
- `published` (Default: True)
- `created_at`
- `owner_id` (Foreign Key to Users)

### Votes Table
- `user_id` (Foreign Key to Users, Primary Key)
- `post_id` (Foreign Key to Posts, Primary Key)

## Installation & Setup

### Prerequisites
- Python 3.12+
- PostgreSQL
- Docker (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-social-media-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the `app` directory:
   ```env
   DATABASE_USERNAME=your_db_user
   DATABASE_HOSTNAME=localhost
   DATABASE_PASSWORD=your_db_password
   DATABASE_PORT=5432
   DATABASE_NAME=your_db_name
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

5. **Database Setup**
   ```bash
   # Run database migrations
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   fastapi run --host 0.0.0.0 --port 8000 app/main.py
   ```

The API will be available at `http://localhost:8000`

### Docker Development

1. **Using Docker Compose**
   ```bash
   docker-compose up --build
   ```

This will start both the FastAPI application and PostgreSQL database.

### Production Deployment

1. **Using production Docker Compose**
   ```bash
   docker-compose -f docker-compose-prod.yml up -d
   ```

Make sure to set your environment variables in a `.env` file for production.

## Database Migrations

This project uses Alembic for database migrations:

```bash
alembic upgrade head
```

## Testing

Run the test suite:

```bash
pytest
```

The test suite includes:
- User authentication tests
- Post CRUD operation tests
- Voting functionality tests
- Authorization and permission tests

## API Documentation

Once the application is running, you can access:
- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`

## Authentication

The API uses JWT tokens for authentication:

1. **Register a new user** via `POST /users/`
2. **Login** via `POST /login` to receive an access token
3. **Include the token** in the Authorization header: `Bearer <your-token>`

## Project Structure

```
├── app/
│   ├── routers/          # API route definitions
│   │   ├── auth.py       # Authentication routes
│   │   ├── post.py       # Post management routes
│   │   ├── user.py       # User management routes
│   │   └── vote.py       # Voting routes
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection setup
│   ├── main.py           # FastAPI application entry point
│   ├── models.py         # SQLAlchemy database models
│   ├── oauth2.py         # JWT token handling
│   ├── schemas.py        # Pydantic schemas for validation
│   └── utils.py          # Utility functions (password hashing)
├── alembic/              # Database migration files
├── tests/                # Test suite
├── docker-compose.yml    # Development Docker setup
├── docker-compose-prod.yml # Production Docker setup
├── Dockerfile            # Docker image configuration
└── requirements.txt      # Python dependencies
```


## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
- Runs tests on every push and pull request
- Builds and pushes Docker images to Docker Hub
