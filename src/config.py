from pathlib import Path
from pyautogui import KEYBOARD_KEYS
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationInfo

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, strict=True)
    
    shutdown_key: str = "q"

    path_to_templates: Path = "templates"
    path_to_product_templates: Path = "templates/products"
    
    @field_validator("shutdown_key", mode="before")
    @classmethod
    def validate_shutdown_key(cls, v: str) -> str:
        if v not in KEYBOARD_KEYS:
            raise ValueError(f"incorrect key {v}")
        return v

    @field_validator("path_to_templates", "path_to_product_templates", mode="before")
    @classmethod
    def convert_path_type(cls, v: str, info: ValidationInfo) -> Path:
        if not isinstance(v, str):
            raise TypeError(f"{info.field_name} must be a string")
        return Path(v)
    
config = Settings()