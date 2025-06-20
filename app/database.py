"""SQLAlchemy用."""

from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel as BasePanel
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from app import const

# データベースのURL
DATABASE_URL = f"mysql+pymysql://{const.DB_USER}:{const.DB_PASS}@{const.DB_HOST}/{const.DB_NAME}?charset=utf8"

# SQLAlchemyでDB接続するための設定
# engine はDB接続のインターフェースとして使われる
engine = create_engine(
    DATABASE_URL,
    echo=False, # SQLのコンソールを非表示
)

# セッション管理を行う？
# セッションのファクトリー関数(？？？？？)
SessionLocal = scoped_session(
    # セッションの作成
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine, # engineを接続
    ),
)

# テーブル定義の基底クラス
Base = declarative_base()


class SQLAlchemyPanel(BasePanel):
    """FastAPI Debug BarにSQLAlchemyクエリ実行結果表示パネルを追加するための記述."""
    async def add_engines(self, _: Request) -> None:  # noqa: D102
        self.engines.add(engine)
