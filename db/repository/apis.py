from sqlalchemy.orm import Session

from schemas.apis import ApiCreate
from db.models.apis import Api


def create_new_api(api: ApiCreate,db : Session,owner_id:int):
    api = api(**api.dict(),owner_id = owner_id)
    db.add(api)
    db.commit()
    db.refresh(api)
    return api


def retreive_api(id:int,db:Session):
    api = db.query(Api).filter(Api.id==id).first()
    return api


def list_apis(db: Session):
    apis = db.query(Api).filter(Api.is_active==True).all()
    return apis


def update_api_by_id(id:int,api:ApiCreate,db:Session,owner_id:int):
    existing_api = db.query(Api).filter(Api.id == id)
    if not existing_api.first():
        return 0
    api.__dict__.update(owner_id=owner_id)
    existing_api.update(api.__dict__)
    db.commit()
    return 1


def delete_api_by_id(id:int,db:Session,owner_id):
    existing_api = db.query(Api).filter(Api.id ==id)
    if not existing_api.first():
        return 0
    existing_api.delete(synchronize_session=False)
    db.commit()
    return 1