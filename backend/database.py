from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql://root:123456@localhost:3306/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL#, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#"mysql://novelpj:HHHeio456868@rm-uf6o0jnw5l424kpphwo.mysql.rds.aliyuncs.com:3306/novelpj"