from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_creator_model: str = "anthropic/claude-sonnet-4"
    openrouter_critic_model: str = "openai/gpt-5.2"
    openrouter_research_model: str = "google/gemini-2.5-pro"
    max_iterations: int = 3
    quality_gate: int = 90

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
