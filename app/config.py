from dotenv import load_dotenv
import os

load_dotenv()


# basic connection configs
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)

    DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://flaskuser:123456@localhost/tododb"
    )
