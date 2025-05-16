import os


DATABASE_HOST: str = str(os.getenv("DATABASE_HOST"))
DATABASE_PORT: str = str(os.getenv("DATABASE_PORT"))
DATABASE_PASSWORD: str = str(os.getenv("DATABASE_PASSWORD"))
DATABASE_USER: str = str(os.getenv("DATABASE_USER"))
DATABASE_NAME: str = str(os.getenv("DATABASE_NAME"))
SECRET_KEY: str = str(os.getenv("SECRET_KEY"))
HASH_ALGORITHM: str = str(os.getenv("HASH_ALGORITHM"))
ACCESS_TOKEN_EXPIRES: str = str(os.getenv("ACCESS_TOKEN_EXPIRES"))
REFRESH_TOKEN_EXPIRES: str = str(os.getenv("REFRESH_TOKEN_EXPIRES"))
GEMINI_TOKEN: str = str(os.getenv("GEMINI_TOKEN"))
