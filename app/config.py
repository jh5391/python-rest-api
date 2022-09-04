from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"
        fields = {
                    'database_hostname': {
                        'env': 'DATABASE_HOSTNAME',
                    },
                    'database_port': {
                        'env': 'DATABASE_PORT',
                    },
                    'database_password': {
                        'env': 'DATABASE_PASSWORD',
                    },
                    'database_name': {
                        'env': 'DATABASE_NAME',
                    },
                    'database_username': {
                        'env': 'DATABASE_USERNAME',
                    },
                    'secret_key': {
                        'env': 'SECRET_KEY',
                    },
                    'algorithm': {
                        'env': 'ALGORITHM',
                    },
                    'access_token_expire_minutes': {
                        'env': 'ACCESS_TOKEN_EXPIRE_MINUTES',
                    },
                }


settings = Settings()
