from pydantic import BaseSettings

class Setting(BaseSettings):

    database_name: str
    database_port: str
    database_password: str
    database_host: str
    database_username: str
    database_driver: str
    secret_key: str
    algorithm: str
    expiry_time: int

    class Config:
        env_file=".env"

