from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import list_schema
from ..crud import list_crud
from ..dependencies import get_db

# '/lists/' から始まるパスになる
router = APIRouter(
    prefix='/lists',
    tags=['Todoリスト'],
)

# POST 作成
@router.post('/', response_model=list_schema.ResponseTodoList)
def post_todo_list(todoList: list_schema.NewTodoList, session: Session = Depends(get_db)):
    todo_list = list_crud.create_todo_post(db=session, new_todo_list=todoList)
    return list_schema.ResponseTodoList(
        id=todo_list.id,
        title=todo_list.title,
        description=todo_list.description,
        created_at=todo_list.created_at,
        updated_at=todo_list.updated_at,
    )

# GET 取得
@router.get('/{todo_list_id}', response_model=list_schema.ResponseTodoList)
def get_todo_list(todo_list_id: int, session: Session = Depends(get_db)):
    todo_list = list_crud.get_todo_list(db=session, todo_list_id=todo_list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail='Todo List not found')
    return list_schema.ResponseTodoList(
        id=todo_list.id,
        title=todo_list.title,
        description=todo_list.description,
        created_at=todo_list.created_at,
        updated_at=todo_list.updated_at,
    )

# GET 全てのTODOリストを取得
@router.get('/', response_model=list[list_schema.ResponseTodoList]) # ResponseTodoListの配列を示す
def get_todo_lists(session: Session = Depends(get_db)):
    todo_lists = list_crud.get_todo_lists(db=session)
    # 一応 ResponseTodoList で返す
    return [list_schema.ResponseTodoList(
        id=todo_list.id,
        title=todo_list.title,
        description=todo_list.description,
        created_at=todo_list.created_at,
        updated_at=todo_list.updated_at,
    ) for todo_list in todo_lists] # リスト内包表記

# PUT 更新
@router.put('/{todo_list_id}', response_model=list_schema.ResponseTodoList, tags=['Todoリスト'])
def put_todo_list(update_todo_list: list_schema.UpdateTodoList, todo_list_id: int, session: Session = Depends(get_db)):
    todo_list = list_crud.update_todo_list(db=session, todo_list_id=todo_list_id, update_todo_list=update_todo_list)
    if not todo_list:
        # HTTPエラーを発生させる
        raise HTTPException(status_code=404, detail='Todo List not found')
    return list_schema.ResponseTodoList(
        id=todo_list.id,
        title=todo_list.title,
        description=todo_list.description,
        created_at=todo_list.created_at,
        updated_at=todo_list.updated_at,
    )

# DELETE 削除
@router.delete('/{todo_list_id}', tags=['Todoリスト'])
def delete_todo_list(todo_list_id: int, session: Session = Depends(get_db)):
    isDelete = list_crud.delete_todo_list(db=session, todo_list_id=todo_list_id)    
    if not isDelete:
        raise HTTPException(status_code=404, detail='Todo List not found')
    return {}