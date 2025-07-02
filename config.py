from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    mssql_host: str
    mssql_port: int
    mssql_user: str
    mssql_password: str
    mssql_db: str
    mssql_driver: str = "{ODBC Driver 18 for SQL Server}"
    mssql_connection_timeout: int = 30

    @property
    def mssql_connection_string(self) -> str:
        return ";".join(
            [
                "Driver={ODBC Driver 18 for SQL Server}",
                f"Server={self.mssql_host},{self.mssql_port}",
                f"Database={self.mssql_db}",
                f"UID={self.mssql_user}",
                f"PWD={self.mssql_password}",
                "Encrypt=yes",
                "TrustServerCertificate=yes",
                f"Connection Timeout={self.mssql_connection_timeout}",
            ]
        )


settings = Settings()  # type: ignore
