from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RETELL_API_KEY: str = ""
    GOOGLE_SERVICE_ACCOUNT_JSON: str = ""
    GOOGLE_SHEET_ID: str = ""
    RESEND_API_KEY: str = ""
    CLINIC_NOTIFY_EMAIL: str = ""
    CLINIC_FROM_EMAIL: str = "onboarding@resend.dev"
    ENV: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
