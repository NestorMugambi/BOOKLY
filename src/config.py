from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def async_database_config(self):
        """Parse the DATABASE_URL for asyncpg configuration."""
        parsed_url = urlparse(self.DATABASE_URL)
        query_params = parse_qs(parsed_url.query)

        sslmode = query_params.get("sslmode", ["require"])[0]  # Default to "require"

        return {
            "driver": "postgresql+asyncpg",
            "username": parsed_url.username,
            "password": parsed_url.password,
            "host": parsed_url.hostname,
            "port": parsed_url.port or 5432,  # Default to port 5432
            "database": parsed_url.path.lstrip("/"),  # Remove leading "/"
            "ssl": sslmode == "require",  # Convert to a boolean for asyncpg
        }

# Initialize configuration
Config = Settings()

# Example usage
db_config = Config.async_database_config
print("Async Database Config:", db_config)
