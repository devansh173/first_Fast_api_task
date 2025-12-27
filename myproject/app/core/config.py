DATABASES = {
    "oracle":  "oracle+cx_oracle://username:password@host:1521/dbname",
    "postgres": "postgresql://username:password@localhost:5432/dbname",
    "mysql":    "mysql+mysqlconnector://username:password@localhost:3306/dbname"
}

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30