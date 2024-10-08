import os
from dotenv import load_dotenv, find_dotenv



BASE_DIR : str = os.getcwd()
ENV_FILE: str = os.path.join(BASE_DIR, ".env")


try:
    import pydantic_settings 
except ModuleNotFoundError:
    raise Exception("No module named pydantic_settings")


class Settings(pydantic_settings.BaseSettings):
    # Pydantic converts field names to uppercase to find corresponding environment variables.
    mistral_api_key: str
    debug: bool

    model_config = pydantic_settings.SettingsConfigDict(env_file=ENV_FILE )

    # def __init__(self):
    #     _ = load_dotenv(find_dotenv(ENV_FILE), override=True) # this line to overwrite the values if they exist

    def str(self):
        print(f"Mistral_API_KEY: {self.mistral_api_key} |  DEBUG: {self.debug}")


def load_settings()-> Settings:
    print(f"Loading .env file")

    if not ENV_FILE:
        raise FileNotFoundError(".env file not found")

    _ = load_dotenv(find_dotenv(ENV_FILE), override=True) # this line to overwrite the values if they exist
    return Settings()


if __name__ == "__main__":
    setting = Settings()
    setting.str()