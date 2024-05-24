from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationInfo


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, strict=True)
    
    pyautogui_failsafe: bool = True
    
    path_to_templates: Path = "templates"
    path_to_products_templates: Path = "templates/products"
    
    @field_validator("path_to_templates", "path_to_products_templates", mode="before")
    @classmethod
    def convert_path_type(cls, v: str, info: ValidationInfo) -> Path:
        if not isinstance(v, str):
            raise TypeError(f"{info.field_name} must be string")
        return Path(v)
    
config = Settings()