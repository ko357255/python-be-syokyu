from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import item_schema
from ..crud import item_crud
from ..dependencies import get_db

# '/lists/' から始まるパスになる
router = APIRouter(
    prefix='/lists/{todo_list_id}', # パスパラメータもprefixに入れられる
    tags=['Todo項目'],
)

# POST Todo項目を作成
@router.post('/items/', response_model=item_schema.ResponseTodoItem)
def post_todo_item(
    todo_list_id: int,
    new_todo_item : item_schema.NewTodoItem,
    session: Session = Depends(get_db)
):
    todo_item = item_crud.create_todo_item(db=session, new_todo_item=new_todo_item, todo_list_id=todo_list_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail='Todo List not found')  
    return item_schema.ResponseTodoItem(
        id=todo_item.id,
        todo_list_id=todo_item.todo_list_id,
        title=todo_item.title,
        description=todo_item.description,
        status_code=todo_item.status_code,
        due_at=todo_item.due_at,
        created_at=todo_item.created_at,
        updated_at=todo_item.updated_at,
    )

# GET todo項目を取得
@router.get('/items/{todo_item_id}', response_model=item_schema.ResponseTodoItem)
def get_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    session: Session = Depends(get_db)
):
    todo_item = item_crud.get_todo_item(db=session, todo_list_id=todo_list_id, todo_item_id=todo_item_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail='Todo Item not found')
    
    return item_schema.ResponseTodoItem(
        id=todo_item.id,
        todo_list_id=todo_item.todo_list_id,
        title=todo_item.title,
        description=todo_item.description,
        status_code=todo_item.status_code,
        due_at=todo_item.due_at,
        created_at=todo_item.created_at,
        updated_at=todo_item.updated_at,
    )

@router.get('/items', response_model=list[item_schema.ResponseTodoItem])
def get_todo_items(todo_list_id: int, session: Session = Depends(get_db)):
    todo_items = item_crud.get_todo_items(db=session, todo_list_id=todo_list_id)
    return [item_schema.ResponseTodoItem(
        id=todo_item.id,
        todo_list_id=todo_item.todo_list_id,
        title=todo_item.title,
        description=todo_item.description,
        status_code=todo_item.status_code,
        due_at=todo_item.due_at,
        created_at=todo_item.created_at,
        updated_at=todo_item.updated_at,
    ) for todo_item in todo_items]

# PUT todo項目を更新
@router.put('/items/{todo_item_id}', response_model=item_schema.ResponseTodoItem)
def put_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    update_todo_item : item_schema.UpdateTodoItem,
    session: Session = Depends(get_db)
): 
    todo_item = item_crud.update_todo_item(
        db=session,
        update_todo_item=update_todo_item,
        todo_item_id=todo_item_id,
        todo_list_id= todo_list_id
    )
    if not todo_item:
        raise HTTPException(status_code=404, detail='Todo Item not found')
    return item_schema.ResponseTodoItem(
        id=todo_item.id,
        todo_list_id=todo_item.todo_list_id,
        title=todo_item.title,
        description=todo_item.description,
        status_code=todo_item.status_code,
        due_at=todo_item.due_at,
        created_at=todo_item.created_at,
        updated_at=todo_item.updated_at,
    )

@router.delete('/items/{todo_item_id}')
def delete_todo_item(todo_list_id: int, todo_item_id: int, session: Session = Depends(get_db)):
    todo_item = item_crud.delete_todo_item(db=session, todo_item_id=todo_item_id, todo_list_id=todo_list_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail='Not Found Todo Item')
    return {"message": "Todo Item deleted successfully"}