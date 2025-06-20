from .database import SessionLocal

# DBのセッションを作る関数？
# これは同期する。asyncで非同期で返すのも作れるらしい。
# SQLAlchemy だと SessionLocal() を使うためこの形式
def get_db():
    # データベースのセッションを生成する
    db = SessionLocal()
    try:
        # yield: 値を一時的に返す（関数はいったん、停止する）
        yield db # セッションを返す
        
    finally: # 処理が戻ってきたら（リクエスト処理が終わったら）
        db.close() # セッションを閉じて解放
