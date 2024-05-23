from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    path_to_templates: Path
    path_to_products_templates: Path
    
    pyautogui_failsafe: bool
    
    @field_validator(
        "path_to_templates", 
        "path_to_products_templates", 
        mode="before"
    )
    @classmethod
    def convert_path_type(cls, v: str) -> Path:
        if not isinstance(v, str):
            raise TypeError("Путь должен быть строкой!")
        return Path(v)
    
config = Settings()