from fastapi import Depends, FastAPI, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from pydantic import BaseModel
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import logging

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    account: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#创建一个认证的依赖
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 根据实际情况设置允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user = crud.get_user_by_account(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    #签发token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_account(db, account=token_data.username )
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_active_user: Annotated[User, Depends(get_current_user)],):
    if not current_active_user.is_admin:
        raise HTTPException(status_code=400, detail="Non-Administrators")
    return current_active_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.account}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, is_admin=user.is_admin, token_type="bearer")

@app.post("/register", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_account = crud.get_user_by_account(db, account=user.account)
    db_user_username = crud.get_user_by_username(db, username=user.username)
    if db_user_account:
        raise HTTPException(status_code=400, detail="account already registered")
    if db_user_username:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User, tags=["users"])
async def show_my_message(current_user: Annotated[User, Depends(get_current_user)],):
    return current_user

@app.get("/admin/users", response_model=list[schemas.User], tags=["users"])
def show_users(
      db: Session = Depends(get_db),
      current_user:User=Depends(get_current_admin_user)):
    if not current_user:
     raise HTTPException(status_code=400, detail="Forbidden")
    users=crud.get_all_users(db)
    return users

@app.get("/userid/{user_id}", response_model=schemas.User, tags=["users"])
def search_user_by_uid(user_id: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)):
    print(user_id)
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/usersname/{user_name}", response_model=schemas.User, tags=["users"])
def search_user_by_username(user_name: str = "string", db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)):
    print(user_name)
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_users = crud.get_user_by_username(db, username=user_name)
    if db_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_users

@app.get("/usersaccount/{user_account}", response_model=schemas.User, tags=["users"])
def search_user_by_account(user_account: str,
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    print(user_account)
    db_users = crud.get_user_by_account(db, account=user_account)
    if db_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_users

@app.get("/novels/{novel_id}/author/", tags=["users"])
async def get_author_of_novel(
    novel_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    return crud.get_author_by_novel_id(db, novel_id)

@app.patch("/users/{user_id}/activate/", tags=["users"])
async def update_user_activation(user_id: int,
                                 current_user: Annotated[User, Depends(get_current_admin_user)],
                                 db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    return crud.update_activate_user(db, user_id)


@app.patch("/users/{user_id}/admin/", tags=["users"])
async def update_user_activation(user_id: int,
                                 current_user: Annotated[User, Depends(get_current_admin_user)],
                                 db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    return crud.update_admin_user(db, user_id)

@app.post("/createnovel/", tags=["novels"])
async def create_novel(
    novel: schemas.NovelCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    print(current_user.id)
    return crud.create_novel(db, novel, current_user.id)

@app.get("/users/me/novels/", tags=["novels"])
async def get_own_novels(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_novels = crud.get_own_novels(db, author_id=current_user.id)
    if db_novels is None:
        raise HTTPException(status_code=404, detail="You do not have any novels")
    return db_novels

@app.get("/shownovels/", tags=["novels"])
async def show_novels(
    db: Session = Depends(get_db)
):
    db_novels = crud.get_novels(db,0,100)
    if db_novels is None:
        raise HTTPException(status_code=404, detail="No novels")
    return db_novels

@app.get("/admin/novels/", tags=["novels"])
async def show_novels(
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_novels = crud.get_all_novels(db)
    if db_novels is None:
        raise HTTPException(status_code=404, detail="No novels")
    return db_novels

@app.get("/novels/by_title/{title_part}", tags=["novels"])
async def search_novels_by_title(
    title_part: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_novels=crud.get_novels_by_title_part(db, title_part)
    if db_novels is None:
        raise HTTPException(status_code=404, detail="no novels")
    return db_novels

@app.get("/novels/by_category/{category}", response_model=list[schemas.Novel], tags=["novels"])
async def search_novels_by_category(
    category: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    try:
        novels = crud.get_novels_by_category(db, category)
        if novels is None:
            raise HTTPException(status_code=404, detail="没有找到该类别的小说")
        return novels
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/novels/word_count/", response_model=list[schemas.Novel], tags=["novels"])
async def search_novels_by_word_count(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    novels = crud.get_novels_by_word_count(db)
    if novels is None:
        raise HTTPException(status_code=404, detail="没有找到符合字数范围的小说")
    return novels

@app.get("/novels/rating/", response_model=list[schemas.Novel], tags=["novels"])
async def search_novels_by_word_count(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    novels = crud.get_novels_by_rating(db)
    if novels is None:
        raise HTTPException(status_code=404, detail="没有找到符合字数范围的小说")
    return novels

@app.get("/novels/finished/", response_model=list[schemas.Novel], tags=["novels"])
async def search_novels_by_word_count(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    novels = crud.get_novels_finished(db)
    if novels is None:
        raise HTTPException(status_code=404, detail="没有找到符合字数范围的小说")
    return novels

@app.get("/novels/by_id/{novel_id}/", tags=["novels"])
async def get_novels_by_id(
    novel_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_novel=crud.get_novel(db, novel_id)
    if db_novel is None:
        raise HTTPException(status_code=404, detail="no novel")
    return db_novel

@app.patch("/novels/{novel_id}/visible/", tags=["novels"])
async def update_novel_visible_status(
        novel_id: int,
        current_user: Annotated[User, Depends(get_current_admin_user)],
        db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_novel = crud.get_novel_admin(db, novel_id)
    if not db_novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    return crud.update_novel_visible_status(db, novel_id)

@app.patch("/novels/{novel_id}/finished/", tags=["novels"])
async def update_novel_finished_status(
        novel_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
):
    db_novel = crud.get_novel(db, novel_id)
    if not db_novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    if db_novel.author_id!= current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.update_novel_finished_status(db, novel_id)

# 章节相关路由
@app.post("/novels/{novel_id}/chapters_create/", response_model=schemas.Chapter, tags=["chapters"])
async def create_chapter(
    chapter: schemas.ChapterCreate,
    novel_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    novel = crud.get_novel(db, novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found or not visible")
    if novel.is_finished:
        raise HTTPException(status_code=403, detail="Forbidden, novel is finished, please adjust the completion status of the novel first.")
    if novel.author_id!= current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden, you are not the author")
    if chapter.chapter_number != novel.current_chapter + 1:
        raise HTTPException(status_code=403, detail="Forbidden, you can only create the next chapter.")
    novel.current_chapter += 1
    db.commit()
    db.refresh(novel)
    return crud.create_chapter(db, chapter, novel_id)

@app.get("/chapters/{chapter_id}", response_model=schemas.Chapter, tags=["chapters"])
async def get_chapter_by_chapter_id(
    chapter_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    chapter = crud.get_chapter(db, chapter_id)
    novel = crud.get_novel(db, chapter.novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found or not visible")
    novel.click_number += 1
    db.commit()
    db.refresh(novel)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.get("/chapter/pre/{chapter_id}", response_model=schemas.Chapter, tags=["chapters"])
async def get_pre_chapter_id(
    chapter_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    chapter = crud.get_pre_chapter(db, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.get("/chapter/after/{chapter_id}", response_model=schemas.Chapter, tags=["chapters"])
async def get_after_chapter_id(
    chapter_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    chapter = crud.get_after_chapter(db, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.get("/novels/{novel_id}/menu/", response_model=list[schemas.Chapter], tags=["chapters"])
async def get_novel_menu_by_novel_id(
    novel_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    novel = crud.get_novel(db, novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found or not visible")
    chapters = crud.get_chapters_by_novel_id(db, novel_id)
    if chapters is None:
        raise HTTPException(status_code=404, detail="No chapters found for this novel")
    return chapters

@app.patch("/chapters/{chapter_id}/update", response_model=schemas.Chapter, tags=["chapters"])
async def update_chapter(
    chapter_id: int, 
    chapter: schemas.Chapter,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Forbidden")
    db_chapter =crud.get_chapter(db, chapter_id)
    novel = crud.get_novel(db, db_chapter.novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found or not visible")
    if novel.author_id!= current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden, you are not the auther of this chapter")
    
    return crud.update_chapter(db, db_chapter, chapter)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, port=8000)