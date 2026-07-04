import sqlite3
from pathlib import Path

from app.core.config import settings


def _sqlite_path() -> Path | None:
    url = settings.DATABASE_URL
    if not url.startswith("sqlite:///"):
        return None
    raw = url.removeprefix("sqlite:///")
    path = Path(raw)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def ensure_gift_commerce_columns() -> None:
    db_path = _sqlite_path()
    if db_path is None or not db_path.exists():
        return

    connection = sqlite3.connect(db_path)
    try:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(gifts)").fetchall()
        }
        if "purchase_url" not in columns:
            connection.execute(
                "ALTER TABLE gifts ADD COLUMN purchase_url VARCHAR(500) DEFAULT ''"
            )
        if "platform" not in columns:
            connection.execute(
                "ALTER TABLE gifts ADD COLUMN platform VARCHAR(20) DEFAULT 'taobao'"
            )
        connection.commit()
    finally:
        connection.close()
