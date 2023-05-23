from pydantic import BaseSettings, SecretStr


class Config(BaseSettings):
    bot_token: SecretStr
    interval_parse: int
    window_app_title: str
    window_width: int
    window_height: int
    window_width_min: int
    window_height_min: int
    window_resizable: bool

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_config() -> Config:
    return Config()
