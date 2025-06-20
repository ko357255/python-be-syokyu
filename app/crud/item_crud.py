from sqlalchemy.orm import Session
from ..schemas.item_schema import NewTodoItem, UpdateTodoItem
from ..models.item_model import ItemModel
from ..models.list_model import ListModel
from app.const import TodoItemStatusCode

def create_todo_item(db: Session, todo_list_id: int, new_todo_item: NewTodoItem):
    """新しいTodo項目を作成する"""
    todo_list = db.query(ListModel).filter_by(id=todo_list_id).first()
    if todo_list is None:
        return None
    
    todo_item = ItemModel(
        title=new_todo_item.title,
        description=new_todo_item.description,
        due_at=new_todo_item.due_at,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
        todo_list_id=todo_list_id,
    )
    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)
    return todo_item

def get_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    """指定したTodoリスト内のTodo項目を取得する"""
    return db.query(ItemModel).filter_by(id=todo_item_id, todo_list_id=todo_list_id).first()

def get_todo_items(db: Session, todo_list_id: int, offset: int, limit: int):
    """offsetとlimitを元に指定したTodoリスト内の全てのTodo項目を取得する"""
    return db.query(ItemModel).filter_by(todo_list_id=todo_list_id).offset(offset).limit(limit).all()

def update_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id: int,
    update_todo_item: UpdateTodoItem,
):
    """指定したTodo項目を更新する"""
    todo_item = db.query(ItemModel).filter_by(id=todo_item_id, todo_list_id=todo_list_id).first()
    if todo_item is None:
        return None
    
    if update_todo_item.title is not None:
        todo_item.title = update_todo_item.title
    if update_todo_item.description is not None:
        todo_item.description = update_todo_item.description
    if update_todo_item.due_at is not None:
        todo_item.due_at = update_todo_item.due_at
    if update_todo_item.complete is not None:
        todo_item.status_code = TodoItemStatusCode.COMPLETED.value if update_todo_item.complete else TodoItemStatusCode.NOT_COMPLETED.value
    db.commit()
    db.refresh(todo_item)
    return todo_item

def delete_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    """指定したTodo項目を削除する"""
    todo_item = db.query(ItemModel).filter_by(id=todo_item_id, todo_list_id=todo_list_id).first()
    if todo_item is None:
        return False
    db.delete(todo_item)
    db.commit()
    return True