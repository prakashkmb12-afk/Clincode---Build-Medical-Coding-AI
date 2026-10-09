from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineSettings(BaseSettings):
    PROJECT_NAME: str = "ClinCode Pipeline Worker"
    
    # Database
    DATABASE_URL: str = "postgresql://clincode:clincode_dev_2026@localhost:5432/clincode"
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_ICD10: str = "icd10"
    QDRANT_COLLECTION_GUIDELINES: str = "coding_guidelines"
    QDRANT_COLLECTION_PRECEDENTS: str = "chart_precedents"
    
    # Redis Queue
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    
    # Model configuration
    NER_MODEL_NAME: str = "Bio_ClinicalBERT-v1.2-onnx"
    ASSERTION_MODEL_NAME: str = "Bio_ClinicalBERT-assertion-v1.0"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


pipeline_settings = PipelineSettings()
