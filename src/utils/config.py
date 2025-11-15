"""
Configuration management for TeklaMCP
Loads environment variables and provides centralized config access
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Centralized configuration class for TeklaMCP
    All settings loaded from environment variables or defaults
    """

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    SRC_ROOT = PROJECT_ROOT / "src"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    CACHE_DIR = PROJECT_ROOT / ".cache"

    # AI API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Optional Cloud Services
    AZURE_VISION_KEY: str = os.getenv("AZURE_VISION_KEY", "")
    AZURE_VISION_ENDPOINT: str = os.getenv("AZURE_VISION_ENDPOINT", "")
    GOOGLE_VISION_KEY: str = os.getenv("GOOGLE_VISION_KEY", "")

    # Vector Database (for RAG)
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "tekla-api-docs")

    # Application Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL_HOURS: int = int(os.getenv("CACHE_TTL_HOURS", "24"))

    # Processing Settings
    AUTO_EXECUTE: bool = os.getenv("AUTO_EXECUTE", "false").lower() == "true"
    PARALLEL_PROCESSING: bool = os.getenv("PARALLEL_PROCESSING", "true").lower() == "true"
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))

    # Code Generation
    CODE_TEMPLATE_DIR: Path = PROJECT_ROOT / "src" / "code_generation" / "templates"

    # Tekla Settings
    TEKLA_VERSION: str = os.getenv("TEKLA_VERSION", "2023")
    TEKLA_API_PATH: str = os.getenv("TEKLA_API_PATH", "C:\\Program Files\\Tekla Structures\\2023.0\\nt\\bin\\plugins")

    # Development
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SAVE_INTERMEDIATE_RESULTS: bool = os.getenv("SAVE_INTERMEDIATE_RESULTS", "true").lower() == "true"

    # AI Model Settings
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "claude-3-5-sonnet-20250929")
    DEFAULT_VISION_MODEL: str = os.getenv("DEFAULT_VISION_MODEL", "claude-3-5-sonnet-20250929")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "8000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))

    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required configuration is present

        Returns:
            bool: True if config is valid

        Raises:
            ValueError: If required config is missing
        """
        errors = []

        # Check required API keys
        if not cls.ANTHROPIC_API_KEY and not cls.OPENAI_API_KEY:
            errors.append("Either ANTHROPIC_API_KEY or OPENAI_API_KEY must be set")

        # Create required directories
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        if cls.CACHE_ENABLED:
            cls.CACHE_DIR.mkdir(exist_ok=True)

        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")

        return True

    @classmethod
    def get_api_key(cls, provider: str = "anthropic") -> str:
        """
        Get API key for specified provider

        Args:
            provider: "anthropic" or "openai"

        Returns:
            API key string
        """
        if provider.lower() == "anthropic":
            return cls.ANTHROPIC_API_KEY
        elif provider.lower() == "openai":
            return cls.OPENAI_API_KEY
        else:
            raise ValueError(f"Unknown provider: {provider}")

    @classmethod
    def print_config(cls):
        """Print current configuration (without exposing secrets)"""
        print("=" * 60)
        print("TeklaMCP Configuration")
        print("=" * 60)
        print(f"Project Root: {cls.PROJECT_ROOT}")
        print(f"Output Dir: {cls.OUTPUT_DIR}")
        print(f"Cache Enabled: {cls.CACHE_ENABLED}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Anthropic API: {'✓ Set' if cls.ANTHROPIC_API_KEY else '✗ Not Set'}")
        print(f"OpenAI API: {'✓ Set' if cls.OPENAI_API_KEY else '✗ Not Set'}")
        print(f"Default Model: {cls.DEFAULT_LLM_MODEL}")
        print(f"Max Workers: {cls.MAX_WORKERS}")
        print(f"Auto Execute: {cls.AUTO_EXECUTE}")
        print("=" * 60)


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"Warning: {e}")


if __name__ == "__main__":
    Config.print_config()
