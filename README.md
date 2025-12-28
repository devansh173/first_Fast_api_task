# FastAPI Multi-Database Project

A FastAPI application with JWT authentication, multi-database support (Oracle, PostgreSQL, MySQL), and efficient large file upload capabilities.

## 🌐 Live Application

**Available at URL:** https://first-fast-api-task.onrender.com

- **Frontend Dashboard:** https://first-fast-api-task.onrender.com/
- **API Documentation (Swagger UI):** https://first-fast-api-task.onrender.com/docs

## Features

- ✅ **JWT-based Authentication** - Secure token-based authentication
- ✅ **Multi-Database Support** - Single endpoint for Oracle, PostgreSQL, and MySQL
- ✅ **Pydantic Validation** - Input validation using Pydantic models
- ✅ **Large File Upload** - Efficient streaming for big files (up to 10GB)
- ✅ **Protected Endpoints** - Database and file upload endpoints require authentication

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
cd myproject
pip install -r ../requirements.txt
```

**Note:** For Oracle database support, you may need to install Oracle Instant Client separately based on your operating system.

## Configuration

Update `app/core/config.py` with your database connection strings:

```python
DATABASES = {
    "oracle":  "oracle+cx_oracle://username:password@host:1521/dbname",
    "postgres": "postgresql://username:password@localhost:5432/dbname",
    "mysql":    "mysql+mysqlconnector://username:password@localhost:3306/dbname"
}

SECRET_KEY = "your-secret-key-here"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## Running the Application

### Local Development

```bash
cd myproject
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

API documentation (Swagger UI): `http://127.0.0.1:8000/docs`

### Production (Render)

The application is deployed and available at: **https://first-fast-api-task.onrender.com**

## API Endpoints

### Authentication

#### 1. Login
**POST** `/auth/login`

Get a JWT access token.

**Request Body (form-data):**
```
username: admin
password: admin123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 2. Verify Token
**GET** `/auth/verify`

Verify if your JWT token is valid.

**Headers:**
```
Authorization: Bearer <your_token>
```

#### 3. Get Current User
**GET** `/auth/me`

Get information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer <your_token>
```

### Database Query

#### Execute Query
**POST** `/db/query`

Execute a SQL query on Oracle, PostgreSQL, or MySQL database.

**Headers:**
```
Authorization: Bearer <your_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "db_type": "postgres",
  "query": "SELECT * FROM users LIMIT 10"
}
```

**With Custom Connection (Optional):**
```json
{
  "db_type": "postgres",
  "query": "SELECT * FROM users LIMIT 10",
  "host": "localhost",
  "port": 5432,
  "database": "mydb",
  "username": "user",
  "password": "pass"
}
```

**Response:**
```json
{
  "status": "success",
  "db_type": "postgres",
  "rows_affected": 10,
  "data": [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Jane"}
  ]
}
```

**Supported Database Types:**
- `oracle` - Oracle Database
- `postgres` - PostgreSQL
- `mysql` - MySQL

### File Upload

#### Upload Large File
**POST** `/upload/bigfile`

Upload large files efficiently using streaming.

**Headers:**
```
Authorization: Bearer <your_token>
Content-Type: multipart/form-data
```

**Request:**
- Form field: `file` (file to upload)

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "example.pdf",
  "file_path": "uploads/example.pdf",
  "size_mb": 15.5,
  "uploaded_by": "admin"
}
```

**Features:**
- Handles files up to 10GB
- Streams in 1MB chunks for memory efficiency
- Automatically creates `uploads/` directory
- Validates file size during upload

## Default Credentials

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Important:** Change these credentials in production!

## Testing with cURL

### Using Production URL (Render)

### 1. Login and get token:
```bash
curl -X POST "https://first-fast-api-task.onrender.com/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 2. Execute database query:
```bash
curl -X POST "https://first-fast-api-task.onrender.com/db/query" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgres",
    "query": "SELECT version()"
  }'
```

### 3. Upload a file:
```bash
curl -X POST "https://first-fast-api-task.onrender.com/upload/bigfile" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@/path/to/your/file.pdf"
```

### Using Local Development URL

Replace `https://first-fast-api-task.onrender.com` with `http://127.0.0.1:8000` in the above examples for local testing.

## Project Structure

```
myproject/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── auth.py                 # JWT authentication logic
│   ├── database.py             # Database connection handling
│   ├── core/
│   │   └── config.py          # Configuration settings
│   ├── routers/
│   │   ├── db_router.py       # Database query endpoint
│   │   └── file_upload.py     # File upload endpoint
│   └── schemas/
│       └── db_schema.py       # Pydantic models
└── requirements.txt
```

## Security Notes

1. **Change SECRET_KEY** in `config.py` for production
2. **Use environment variables** for sensitive data (passwords, keys)
3. **Implement rate limiting** for production
4. **Use HTTPS** in production
5. **Validate SQL queries** - Consider implementing query whitelisting for production
6. **Store user credentials** in a database instead of hardcoding

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-jose` - JWT token handling
- `bcrypt` - Password hashing
- `sqlalchemy` - Database ORM
- `pydantic` - Data validation
- `psycopg2-binary` - PostgreSQL driver
- `mysql-connector-python` - MySQL driver
- `cx_Oracle` - Oracle driver

## License

This project is for educational/demonstration purposes.
