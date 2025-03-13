from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    account = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    username = Column(String(100))
    is_admin = Column(Boolean, default=False)
    novels = relationship("Novel", back_populates="author")

class Novel(Base):
    __tablename__ = 'novels'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    summary = Column(String(255))
    is_visible = Column(Boolean, default=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    author_name = Column(String(255))
    author = relationship("User", back_populates="novels")
    current_chapter = Column(Integer)
    rating = Column(Integer, default=0.0)
    category = Column(String(50), default='未分类') 
    is_finished = Column(Boolean, default=False)
    word_count = Column(Integer, default=0)
    click_number = Column(Integer, default=0)
    chapters = relationship("Chapter", back_populates="novel")

class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column(Integer, primary_key=True)
    novel_id = Column(Integer, ForeignKey('novels.id'))
    chapter_name = Column(String(255))
    chapter_content = Column(Text)
    chapter_number = Column(Integer)
    word_count = Column(Integer)
    novel = relationship("Novel", back_populates="chapters")