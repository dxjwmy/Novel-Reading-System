from sqlalchemy.orm import Session
from sql_app import models, schemas
from passlib.context import CryptContext
from sqlalchemy import desc
import random

#创建一个加密对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_account(db: Session, account: str):
    return db.query(models.User).filter(models.User.account == account).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_author_by_novel_id(db: Session, novel_id: int):
    novel = db.query(models.Novel).filter(models.Novel.id == novel_id).first()
    if novel:
        return db.query(models.User).filter(models.User.id == novel.author_id).first()
    return None

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(account=user.account, hashed_password=fake_hashed_password, username=user.username)
    if db_user.id == 1:
        db_user.is_admin = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_activate_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        db.commit()
        db.refresh(user)
    return user

def update_admin_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        if user.is_admin:
            user.is_admin = False
        else:
            user.is_admin = True
        db.commit()
        db.refresh(user)
    return user

def get_novel(db: Session, novel_id: int):
    novel = db.query(models.Novel).filter(models.Novel.id == novel_id, models.Novel.is_visible == True).first()
    return novel

def get_novel_admin(db: Session, novel_id: int):
    return db.query(models.Novel).filter(models.Novel.id == novel_id).first()

def get_novels_by_title_part(db: Session, title_part: str):
    return db.query(models.Novel).filter(models.Novel.title.like(f'%{title_part}%'), models.Novel.is_visible == True).all()

def get_novels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Novel).filter(models.Novel.is_visible == True).offset(skip).limit(limit).all()

def get_all_novels(db: Session):
    return db.query(models.Novel).all()

def get_novels_un_visible(db: Session):
    return db.query(models.Novel).filter(models.Novel.is_visible == False).all()

def get_own_novels(db: Session, author_id: int):#不需要管是否可见
    return db.query(models.Novel).filter(models.Novel.author_id == author_id).all()

def get_novels_by_userid(db: Session, author_id: int):
    return db.query(models.Novel).filter(models.Novel.author_id == author_id, models.Novel.is_visible == True).all()

def get_novels_by_category(db: Session, category: str):
    return db.query(models.Novel).filter(models.Novel.category == category, models.Novel.is_visible == True).all()

def get_novels_by_word_count(db: Session):
    return db.query(models.Novel).filter(models.Novel.is_visible == True).order_by(desc(models.Novel.word_count)).all()

def get_novels_by_rating(db: Session):
    return db.query(models.Novel).filter(models.Novel.is_visible == True).order_by(desc(models.Novel.rating)).all()

def get_novels_finished(db: Session):
    return db.query(models.Novel).filter(models.Novel.is_visible == True, models.Novel.is_finished == True).order_by(desc(models.Novel.rating)).all()

def create_novel(db: Session, novel: schemas.NovelCreate, author_id: int):
    rating = random.randint(1, 100)
    author = get_user(db, author_id)
    db_novel = models.Novel(title=novel.title,
                            summary=novel.summary,
                            author_id=author_id,
                            author_name=author.username,
                            category=novel.category,
                            rating=rating,
                            current_chapter=0,
                            is_visible=True,
                            is_finished=False,
                            word_count=0,
                            click_number=0)
    db.add(db_novel)
    db.commit()
    db.refresh(db_novel)
    return db_novel

def increase_novel_number(db: Session, novel_id: int, number: int):
    novel = db.query(models.Novel).filter(models.Novel.id == novel_id).first()
    if novel:
        novel.word_count += number
        db.commit()
        db.refresh(novel)
    return novel

def update_novel_visible_status(db: Session, novel_id: int):
    db_novel = get_novel_admin(db, novel_id)
    if db_novel:
        if db_novel.is_visible:
            db_novel.is_visible = False
        else:
            db_novel.is_visible = True
        db.commit()
        db.refresh(db_novel)
        return db_novel
    return None


def update_novel_finished_status(db: Session, novel_id: int):
    db_novel = get_novel(db, novel_id)
    if db_novel:
        if(db_novel.is_finished ):
            db_novel.is_finished = False
        else:
            db_novel.is_finished = True
        db.commit()
        db.refresh(db_novel)
        return db_novel
    return None

def get_chapter(db: Session, chapter_id: int):
    return db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()

def get_pre_chapter(db: Session, chapter_id: int):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        return None
    pre_chapter_number = chapter.chapter_number - 1
    if pre_chapter_number < 1:
        return chapter
    return db.query(models.Chapter).filter(models.Chapter.chapter_number == pre_chapter_number, models.Chapter.novel_id == chapter.novel_id).first()

def get_after_chapter(db: Session, chapter_id: int):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        return None
    next_chapter_number = chapter.chapter_number + 1
    next_chapter = db.query(models.Chapter).filter(models.Chapter.chapter_number == next_chapter_number, models.Chapter.novel_id == chapter.novel_id).first()
    if not next_chapter:
        return chapter
    return next_chapter

def get_chapters_by_novel_id(db: Session, novel_id: int):
    return db.query(models.Chapter).filter(models.Chapter.novel_id == novel_id).all()

def create_chapter(db: Session, chapter: schemas.ChapterCreate, n_id: int):
    word_count = len(chapter.chapter_content)
    db_chapter = models.Chapter(novel_id=n_id, chapter_name=chapter.chapter_name, chapter_content=chapter.chapter_content, chapter_number=chapter.chapter_number, word_count=word_count)
    db_chapter.word_count = word_count
    increase_novel_number(db, n_id, word_count)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    increase_novel_number(db, n_id, word_count)
    return db_chapter

def update_chapter(db: Session, db_chapter: models.Chapter, chapter: schemas.Chapter):

    if db_chapter:
        db_chapter.chapter_name = chapter.chapter_name
        db_chapter.chapter_content = chapter.chapter_content
        db_chapter.chapter_number = chapter.chapter_number
        db_chapter.word_count = chapter.word_count
        db.commit()
        db.refresh(db_chapter)
        return db_chapter
    return None