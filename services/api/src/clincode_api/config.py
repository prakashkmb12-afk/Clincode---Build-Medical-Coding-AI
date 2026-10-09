from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ClinCode API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://clincode:clincode_dev_2026@localhost:5432/clincode"
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_ICD10: str = "icd10"
    QDRANT_COLLECTION_GUIDELINES: str = "coding_guidelines"
    QDRANT_COLLECTION_PRECEDENTS: str = "chart_precedents"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    
    # JWT Authentication
    JWT_SECRET: str = "super-secret-clincode-jwt-key-change-in-prod-2026!"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # PHI Encryption
    FERNET_KEY: str = "3X-sX-s3Z4Z_X_s3Z4Z_X_s3Z4Z_X_s3Z4Z_X_s3Z4Z="
    
    # LLM & AI
    OPENAI_API_KEY: str = "mock-key-for-local-testing"
    LLM_MODEL: str = "gpt-4o-mini"
    MOCK_LLM: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
