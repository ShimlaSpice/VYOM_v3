from pathlib import Path

from app.database import Database, Repositories, create_all_tables
from config.manager import ConfigManager
from config.settings import Settings


def test_create_all_tables_returns_repositories(tmp_path: Path) -> None:
    database = Database(tmp_path / "vyom_test.db")

    repositories = create_all_tables(database)

    assert isinstance(repositories, Repositories)
    assert repositories.market is not None
    assert repositories.recommendation is not None
    assert repositories.trade is not None
    assert repositories.portfolio is not None


def test_config_manager_returns_settings_instance() -> None:
    manager = ConfigManager()
    settings = manager.settings

    assert isinstance(settings, Settings)
    assert manager.settings is settings
