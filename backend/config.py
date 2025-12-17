import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(
        default=os.getenv("DATABASE_URL", "mysql+pymysql://user:password@db:3306/pharma")
    )
    openai_api_key: str = Field(default=os.getenv("OPENAI_API_KEY", ""))
    enable_llm: bool = Field(default=bool(os.getenv("OPENAI_API_KEY")))
    mock_iqvia_url: str = Field(default=os.getenv("MOCK_IQVIA_URL", "https://mock.api/iqvia"))
    mock_exim_url: str = Field(default=os.getenv("MOCK_EXIM_URL", "https://mock.api/exim"))
    mock_patent_url: str = Field(default=os.getenv("MOCK_PATENT_URL", "https://mock.api/patents"))
    mock_trials_url: str = Field(default=os.getenv("MOCK_TRIALS_URL", "https://mock.api/trials"))
    internal_docs_path: str = Field(default=os.getenv("INTERNAL_DOCS_PATH", "/data/internal_docs"))
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))


settings = Settings()

