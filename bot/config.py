from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    pyautogui_failsafe: bool
    
if __name__ == "__main__":
    settings = Settings()
    print(settings.model_fields)