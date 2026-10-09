from pydantic_settings import BaseSettings, SettingsConfigDict


class InvestigatorSettings(BaseSettings):
    PROJECT_NAME: str = "ClinCode Multi-Agent Investigator Service"
    
    # Database
    DATABASE_URL: str = "postgresql://clincode:clincode_dev_2026@localhost:5432/clincode"
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_ICD10: str = "icd10"
    QDRANT_COLLECTION_GUIDELINES: str = "coding_guidelines"
    QDRANT_COLLECTION_PRECEDENTS: str = "chart_precedents"
    
    # LLM Settings
    OPENAI_API_KEY: str = "mock-key-for-local-testing"
    LLM_MODEL: str = "gpt-4o-mini"
    MOCK_LLM: bool = True
    
    # Budget limits
    MAX_TOOL_CALLS: int = 12
    MAX_REVISION_LOOPS: int = 2
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


investigator_settings = InvestigatorSettings()
