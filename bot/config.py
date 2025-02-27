from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Конфигурация Pydantic
    model_config = SettingsConfigDict(
        env_file="../.env",  # Указываем, что переменные окружения загружаются из .env файла
        env_file_encoding="utf-8",  # Указываем кодировку файла
        case_sensitive=False,  # Не учитывать регистр
    )

    bot_token: str


# Создаем объект настроек
settings = Settings()
print(settings.bot_token)

# Теперь можно использовать settings.bot_token
# print(f"Bot token: {settings.bot_token}")