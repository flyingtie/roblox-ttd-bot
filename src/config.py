from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    pyautogui_failsafe: bool = True