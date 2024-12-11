from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.models import review # 导入所有模型
# from app.routers.review_service import review_router  # 导入评论相关的 router
# 
from strawberry.asgi import GraphQL
from app.routers.review_service import schema
# 
# from app.routers.review_service import review_router  # 导入评论相关的 router
from app.config.log import setup_logger
from app.dependecies.logging_middleware import logging_dependency
# 创建数据库表
review.Base.metadata.create_all(bind=engine)

logger = setup_logger()


app = FastAPI()


# # 这是一个router的示例
# app.include_router(review_router, prefix="/reviews", tags=["reviews"])


graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
# 这是一个router的示例
# app.include_router(review_router, prefix="/reviews", tags=["reviews"])
app.middleware("http")(logging_dependency)

@app.get("/")
def read_root():
    return {"Hello": "World"}
# 

# 
