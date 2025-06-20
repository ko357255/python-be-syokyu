from typing import ClassVar

from sqlalchemy import Column, DateTime, Integer, String, func, text
from sqlalchemy.orm import relationship

from app.database import Base

# SQLAlchemy(ORM)でのデータベースモデルの定義
class ListModel(Base):
    """TODOリストモデル."""

    # テーブル名
    __tablename__ = "todo_lists"
    # コメント？ 型ヒント: ClassVar[dict[str]] → Record<string, string> みたいなもん
    __table_args__: ClassVar[dict[str]] = {
        "comment": "TODOリストテーブル",
    }

    # カラムの設定
    # int型 主キー:true オートインクリメント: true
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    # str型(50文字) null許容:false
    title = Column("title", String(50), nullable=False)
    # str型(200文字) null許容:true
    description = Column("description", String(200))
    # datetime型 タイムスタンプを自動付与する
    created_at = Column("created_at", DateTime, server_default=func.now())
    # datetime型 データ更新のたびにタイムスタンプを更新する
    updated_at = Column("updated_at", DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    
    # リレーションシップの設定
    # 複数のItemModelを持つ Itemから親のListModelを取れるようにする
    items = relationship("ItemModel", backref="todo_lists")
