from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import responses, status
from fastapi.security.utils import get_authorization_scheme_param
from db.repository.apis import list_apis
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends
from db.repository.apis import retreive_api

from db.models.users import User
from apis.version1.route_login import get_current_user_from_token
from webapps.apis.forms import ApiCreateForm
from schemas.apis import ApiCreate
from db.repository.apis import create_new_api


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
def home(request:Request,db:Session = Depends(get_db),msg:str = None):
    apis = list_apis(db=db)
    return templates.TemplateResponse("apis/homepage.html",{"request":request,"apis":apis,"msg":msg})


@router.get("/detail/{id}")
def api_detail(id:int, request:Request,db:Session = Depends(get_db)):
    api = retreive_api(id=id, db=db)
    return templates.TemplateResponse("apis/detail.html", {"request":request,
    "api":api})


@router.get("/post-a-api/")
def create_api(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("apis/create_api.html", {"request": request})


@router.post("/post-a-api/")
async def create_api(request: Request, db: Session = Depends(get_db)):
    form = ApireateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            api = ApiCreate(**form.__dict__)
            api = create_new_api(api=api, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/detail/{api.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("apis/create_api.html", form.__dict__)
    return templates.TemplateResponse("apis/create_api.html", form.__dict__)


@router.get("/delete-api/")
def show_apis_to_delete(request: Request,db : Session = Depends(get_db)):
    apis = list_apis(db=db)
    return templates.TemplateResponse("apis/show_apis_to_delete.html", {
        "request":request,
        "apis":apis
    })
