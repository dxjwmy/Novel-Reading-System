from pydantic import BaseModel

class UserBase(BaseModel):
    account: str

class UserCreate(UserBase):
    password: str
    username: str

class User(UserBase):
    id: int
    is_active: bool
    username: str
    is_admin: bool
    novels: list['Novel']  # 如果需要包含小说信息
    class Config:
        from_attributes = True

class NovelBase(BaseModel):
    title: str

class NovelCreate(NovelBase):
    summary: str
    category: str

class Novel(NovelBase):
    id: int
    summary: str
    is_visible: bool
    author_id: int
    author_name: str
    current_chapter: int
    rating: int  
    category: str
    is_finished: bool
    word_count: int
    click_number: int
    class Config:
        from_attributes = True

class ChapterBase(BaseModel):
    chapter_name: str
    chapter_content: str
    chapter_number: int

class ChapterCreate(ChapterBase):
    pass

class Chapter(ChapterBase):
    id: int
    word_count: int
    novel_id: int
    class Config:
        from_attributes = True