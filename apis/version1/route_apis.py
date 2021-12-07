from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.apis import Api
from schemas.apis import ApiCreate,ShowApi
from db.repository.apis import (create_new_api,
        retreive_api,list_apis,
        update_api_by_id,
        delete_api_by_id)
from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from typing import List

router = APIRouter()


@router.post("/create-api",response_model=ShowApi)
def create_api(api : ApiCreate,db : Session = Depends(get_db),current_user: User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    api = create_new_api(api=api, db=db, owner_id=owner_id)
    return api


@router.get("/get/{id}",response_model=ShowApi)
def retreive_api_by_id(id:int,db:Session = Depends(get_db)):
    api = retreive_api(id=id, db=db)
    print(api)
    if not api:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"api with id {id} does not exist")
    return api


@router.get("/all",response_model=List[ShowApi])
def retreive_all_apis(db:Session = Depends(get_db)):
    apis = list_apis(db=db)
    return apis


@router.put("/update/{id}")
def update_api(id:int,api:ApiCreate,db:Session=Depends(get_db),current_user: User=Depends(get_current_user_from_token)):
    owner_id = current_user.id
    api_retrieved = retreive_api(id=id, db=db)
    if not api_retrieved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"api with id {id} does not exist")
    if api_retrieved.owner_id == current_user.id or current_user.is_superuser:
        message = update_api_by_id(id=id, api=api, db=db, owner_id=owner_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not authorized to update.")
    return {"detail":"Successfully updated data."}


@router.delete("/delete/{id}")
def delete_api(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user_from_token)):
    api = retreive_api(id=id, db=db)
    if not api:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"api with id {id} does not exist")
    if api.owner_id == current_user.id or current_user.is_superuser:
        delete_api_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail":"api Successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not permitted!!")