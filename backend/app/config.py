from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    database_url: str = "postgresql://postgres:postgres@localhost:5433/memory_layer"
    port: int = 8000
    embedding_model: str = "text-embedding-3-small"
    extraction_model: str = "gpt-4o"
    evaluation_model: str = "gpt-4o"
    response_model: str = "gpt-4o"
    embedding_dimensions: int = 1536
    retrieval_top_k: int = 5
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
