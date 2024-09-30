from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.models import review # 导入所有模型
from app.routers.review_service import review_router  # 导入评论相关的 router

# 创建数据库表
review.Base.metadata.create_all(bind=engine)



app = FastAPI()


# 这是一个router的示例
app.include_router(review_router, prefix="/reviews", tags=["reviews"])

@app.get("/")
def read_root():
    return {"Hello": "World"}