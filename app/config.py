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
#        env_file = "../.env"'
        fields = {
                    'database_hostname': {
                        'env': 'database_hostname',
                    },
                    'database_port': {
                        'env': 'database_port',
                    },
                    'database_password': {
                        'env': 'database_password',
                    },
                    'database_name': {
                        'env': 'database_name',
                    },
                    'database_username': {
                        'env': 'database_username',
                    },
                    'secret_key': {
                        'env': 'secret_key',
                    },
                    'algorithm': {
                        'env': 'algorithm',
                    },
                    'access_token_expire_minutes': {
                        'env': 'access_token_expire_minutes',
                    },
                }


settings = Settings()
