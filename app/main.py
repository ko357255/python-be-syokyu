import os
from fastapi import FastAPI

from .routers import list_router, item_router

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )

# routers のルートを設定する
app.include_router(list_router.router) # TODOリスト
app.include_router(item_router.router) # TODO項目


# エコー
@app.get("/echo", tags=["echo"])
def get_echo(message: str, name: str):
    return {"Message": f'{message} {name}!'}

# ヘルスチェック用
@app.get('/health', tags=['System'])
def get_health():
    return {'status': 'ok'}










### 以下API関数は routers, crud に分解 ###

# todoリスト詳細を取得
# @app.get('/lists/{todo_list_id}', tags=['Todoリスト'], response_model=ResponseTodoList)
# def get_todo_list(todo_list_id: int, session: Session = Depends(get_db)):
#     # session: Session = Depends(get_db) でも同じ意味になる
    
#     # session: セッションが入ってる
#     # Depends(): 依存関係注入(?)のために使う、意味不明
#     #          : API関数が呼び出されたときに、get_db()してくれる？
#     #          : リクエスト処理(この関数)が終わった後、get_dbのclose()をしてくれるようになる？
    
#     # データ取得
#     db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    
#     if not db_item:
#         raise HTTPException(status_code=404, detail='Todo List not found')
    
#     return ResponseTodoList(
#         id=db_item.id,
#         title=db_item.title,
#         description=db_item.description,
#         created_at=db_item.created_at,
#         updated_at=db_item.updated_at,
#     )
    
#     # ↑のほうが型安全で良い
#     return {
#         'id': db_item.id,
#         'title': db_item.title,
#         "description": db_item.description,
#         "created_at": db_item.created_at,
#         "updated_at": db_item.updated_at,
#     }

# todoリストを作成
# response_model: 返す値のスキーマ
# @app.post('/lists', response_model=ResponseTodoList, tags=['Todoリスト'])
# def post_todo_list(todoList: NewTodoList, session: Session = Depends(get_db)):
#     # todoList: リクエストボディのスキーマ
    
#     # todoリストのインスタンスを生成
#     db_item = ListModel(title=todoList.title, description=todoList.description)
#     # データ追加
#     session.add(db_item)
#     # コミット
#     session.commit()
#     # DBで保存した後の値を再取得する？(idとかcreated_at)
#     session.refresh(db_item)
    
#     return ResponseTodoList(
#         id=db_item.id,
#         title=db_item.title,
#         description=db_item.description,
#         created_at=db_item.created_at,
#         updated_at=db_item.updated_at,
#     )

# todoリストを更新
# @app.put('/lists/{todo_list_id}', response_model=ResponseTodoList, tags=['Todoリスト'])
# def put_todo_list(todoList: UpdateTodoList, todo_list_id: int, session: Session = Depends(get_db)):
#     # FastAPIが自動判断するらしい
#     # BaseModelを継承したスキーマ → リクエストボディ
#     # パスに{}がある → パスパラメータ
#     # シンプル型(str,int,etc..) → クエリパラメータ
    
#     # session.query(テーブル)
#     db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    
#     # もしデータがないなら
#     if not db_item:
#         # HTTPエラーを発生させる
#         raise HTTPException(status_code=404, detail='Todo List not found')
    
#     if todoList.title is not None:
#         db_item.title = todoList.title
#     if todoList.description is not None:
#         db_item.description = todoList.description
    
#     # 保存
#     session.commit()
#     session.refresh(db_item)
    
#     return ResponseTodoList(
#         id=db_item.id,
#         title=db_item.title,
#         description=db_item.description,
#         created_at=db_item.created_at,
#         updated_at=db_item.updated_at,
#     )


# todoリストを削除
# @app.delete('/lists/{todo_list_id}', tags=['Todoリスト'])
# def delete_todo_list(todo_list_id: int, session: Session = Depends(get_db)):
    
#     # session.query(テーブル)
#     db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    
#     if not db_item:
#         raise HTTPException(status_code=404, detail='Todo List not found')
    
#     session.delete(db_item)
#     session.commit()
    
#     return {}


# todo項目を取得
# @app.get('/lists/{todo_list_id}/items/{todo_item_id}', response_model=ResponseTodoItem, tags=['Todo項目'])
# def get_todo_item(
#     todo_list_id: int,
#     todo_item_id: int,
#     session: Session = Depends(get_db)
# ):
#     # filter_by(): モデルを指定せず、(X=YY)のように「=」だけ使える
    
#     todo_item = session.query(ItemModel).filter_by(
#         id=todo_item_id, # item_idが一致
#         todo_list_id=todo_list_id # list_idが一致  
#     ).first()
    
#     if not todo_item:
#         raise HTTPException(status_code=404, detail='Todo Item not found')
    
#     return ResponseTodoItem(
#         id=todo_item.id,
#         todo_list_id=todo_item.todo_list_id,
#         title=todo_item.title,
#         description=todo_item.description,
#         status_code=todo_item.status_code,
#         due_at=todo_item.due_at,
#         created_at=todo_item.created_at,
#         updated_at=todo_item.updated_at,
#     )


# Todo項目を作成
# @app.post('/lists/{todo_list_id}/items', response_model=ResponseTodoItem, tags=['Todo項目'])
# def post_todo_item(
#     todo_list_id: int,
#     new_todo_item : NewTodoItem,
#     session: Session = Depends(get_db)
# ):
    
#     todo_list = session.query(ListModel).filter_by(id = todo_list_id).first()
    
#     if not todo_list:
#         raise HTTPException(status_code=404, detail='Todo List not found')
    
#     # 新しいTodo項目のインスタンスを生成
#     todo_item = ItemModel(
#         title=new_todo_item.title,
#         description=new_todo_item.description,
#         due_at=new_todo_item.due_at,
#         status_code=TodoItemStatusCode.NOT_COMPLETED.value,
#         todo_list_id=todo_list_id, # リストID(外部キー)
#     )
    
#     # DBに追加
#     session.add(todo_item)
#     session.commit()
#     session.refresh(todo_item)
    
#     return ResponseTodoItem(
#         id=todo_item.id,
#         todo_list_id=todo_item.todo_list_id,
#         title=todo_item.title,
#         description=todo_item.description,
#         status_code=todo_item.status_code,
#         due_at=todo_item.due_at,
#         created_at=todo_item.created_at,
#         updated_at=todo_item.updated_at,
#     )


# todo項目を更新
# @app.put('/lists/{todo_list_id}/items/{todo_item_id}', response_model=ResponseTodoItem, tags=['Todo項目'])
# def put_todo_item(
#     todo_list_id: int,
#     todo_item_id: int,
#     update_todo_item : UpdateTodoItem,
#     session: Session = Depends(get_db)
# ):
    
#     todo_item = session.query(ItemModel).filter_by(
#         id=todo_item_id, # item_idが一致
#         todo_list_id=todo_list_id # list_idが一致  
#     ).first()
    
#     if not todo_item:
#         raise HTTPException(status_code=404, detail='Todo Item not found')
    
#     if update_todo_item.title is not None:
#         todo_item.title = update_todo_item.title
#     if update_todo_item.description is not None:
#         todo_item.description = update_todo_item.description
#     if update_todo_item.due_at is not None:
#         todo_item.due_at = update_todo_item.due_at
#     if update_todo_item.complete is not None:
#         todo_item.status_code = TodoItemStatusCode.COMPLETED.value if update_todo_item.complete else TodoItemStatusCode.NOT_COMPLETED.value
    
#     session.commit()
#     session.refresh(todo_item)
    
#     return ResponseTodoItem(
#         id=todo_item.id,
#         todo_list_id=todo_item.todo_list_id,
#         title=todo_item.title,
#         description=todo_item.description,
#         status_code=todo_item.status_code,
#         due_at=todo_item.due_at,
#         created_at=todo_item.created_at,
#         updated_at=todo_item.updated_at,
#     )

# @app.delete('/lists/{todo_list_id}/items/{todo_item_id}', tags=['Todo項目'])
# def delete_todo_item(todo_list_id: int, todo_item_id: int, session: Session = Depends(get_db)):
    
#     todo_item = session.query(ItemModel).filter_by(id=todo_item_id, todo_list_id=todo_list_id).first()
    
#     if todo_item is None:
#         raise HTTPException(status_code=404, detail='Not Found Todo Item')
    
#     session.delete(todo_item)
#     session.commit()
    
#     return {}