from sqlalchemy.orm import Session
from ..schemas.list_schema import NewTodoList, UpdateTodoList
from ..models.list_model import ListModel

# ↑ __init__.py があるフォルダは、まとめてモジュールとしてimportできる

# Sessionを受け取り、単にデータを返すだけの関数にする
# HTTPエラー等は呼び出し元のrouterで行う

def create_todo_post(db: Session, new_todo_list: NewTodoList):
    """新しいTodoリストを作成する"""
    db_item = ListModel(title=new_todo_list.title, description=new_todo_list.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_todo_list(db: Session, todo_list_id: int):
    """指定したIDのTodoリストを取得する"""
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()

def get_todo_lists(db: Session, offset: int, limit: int):
    """offsetとlimitを元に全てのTodoリストを取得する"""
    return db.query(ListModel).offset(offset).limit(limit).all()


def update_todo_list(db: Session, todo_list_id: int, update_todo_list: UpdateTodoList):
    """指定したIDのTodoリストを更新する"""
    todo_list = db.query(ListModel).filter_by(id=todo_list_id).first()
    if todo_list is None:
        return None
    
    if update_todo_list.title is not None:
        todo_list.title = update_todo_list.title
    if update_todo_list.description is not None:
        todo_list.description = update_todo_list.description
    db.commit()
    db.refresh(todo_list)
    return todo_list

def delete_todo_list(db: Session, todo_list_id: int):
    """指定したIDのTodoリストを削除する"""
    todo_list = db.query(ListModel).filter_by(id=todo_list_id).first()
    if todo_list is None:
        return False
    db.delete(todo_list)
    db.commit()
    return True
