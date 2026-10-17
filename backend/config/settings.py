import os
from pathlib import Path
from typing import List, Optional,Literal

from pydantic import  Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # This is the root of the project (two levels up from this file)

class Settings(BaseSettings):

    app_name : str = "Meridian AI - Procurement Intelligence"
    app_env : str = Field(default="local", validation_alias="ENVIRONMENT")  # "local" or "cloud"
    app_version: str = "1.1.0"

    app_mode : Literal["local", "cloud"] = Field(default="local", validation_alias="APP_MODE")  # "local" or "cloud"

    OPENAI_API_KEY: str = Field("", validation_alias="OPENAI_API_KEY")
    llm_model_name: str = Field(default="gpt-6-luna", validation_alias="OPENAI_LLM_MODEL_NAME")
    llm_temperature: float = Field(default=0.0, validation_alias="LLM_TEMPERATURE")
    embedding_model_name: str = Field(default="text-embedding-3", validation_alias="LOCAL_EMBEDDING_MODEL_NAME")
    embedding_dimensions: int = Field(default=1536, validation_alias="LOCAL_EMBEDDING_DIMENSIONS")

    local_data_dir: str = Field(str(PROJECT_ROOT / ".meridian"))
    chroma_collection: str = Field("meridian_docs", validation_alias="CHROMA_COLLECTION")






    model_config = SettingsConfigDict(
        env_file="PROJECT_ROOT/.env",
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore")

    @property
    def is_cloud_mode(self) -> bool:
        return self.app_mode == "cloud"

    @property
    def is_local_mode(self) -> bool:
        return self.app_mode == "local"

    @property
    def chroma_dir(self) -> Path:
        return os.path.join(self.local_data_dir, "chroma")# Directory for Chroma vector store    

    @property
    def local_upload_dir(self) -> Path:
        return os.path.join(self.local_data_dir, "uploads")  # Directory for local file uploads 

settings = Settings()  # Create a single instance of the Settings class to be used throughout the application

if __name__ == "__main__":
    # For testing purposes, print the settings
    print(settings.dict())
    print(f"Chroma directory: {settings.chroma_dir}")
    print(f"Local upload directory: {settings.local_upload_dir}")