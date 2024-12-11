# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime
# from pydantic import BaseModel
# from typing import Optional, List
# import enum
# from app.models.review import Review
# from app.database import get_db

# # Enums for ReviewType and ReviewStatus

# class ReviewStatus(enum.Enum):
#     PENDING = "pending"
#     APPROVED = "approved"
#     REJECTED = "rejected"

# class ReviewType(enum.Enum):
#     PRODUCT = "product"
#     STORE = "store"
#     SERVICE = "service"

# review_router = APIRouter()

# class ReviewCreate(BaseModel):
#     user_id: str
#     review_type: str
#     target_id: str
#     rating: int
#     content: Optional[str] = ""
#     status: Optional[str] = "pending"
#     extra: Optional[dict] = {}

# class ReviewUpdate(BaseModel):
#     rating: Optional[int]
#     content: Optional[str]
#     status: Optional[str]
#     extra: Optional[dict]

# class ReviewResponse(BaseModel):
#     message: str
#     review_id: str

# class StatusResponse(BaseModel):
#     status: str

# class ReviewDetail(BaseModel):
#     id: str
#     user_id: str
#     review_type: str
#     target_id: str
#     rating: int
#     content: str
#     status: str
#     created_at: datetime
#     updated_at: datetime
#     extra: Optional[dict] = {}

# @review_router.post("/reviews", response_model=ReviewResponse)
# def create_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
#     new_review = Review(
#         user_id=review_data.user_id,
#         review_type=review_data.review_type,
#         target_id=review_data.target_id,
#         rating=review_data.rating,
#         content=review_data.content,
#         status=review_data.status,
#         created_at=datetime.utcnow(),
#         updated_at=datetime.utcnow(),
#         extra=review_data.extra or {}
#     )
#     db.add(new_review)
#     db.commit()
#     db.refresh(new_review)
#     return ReviewResponse(message="Review created successfully", review_id=new_review.id)

# @review_router.get("/reviews/{review_id}", response_model=ReviewDetail)
# def get_review(review_id: str, db: Session = Depends(get_db)):
#     review = db.query(Review).filter(Review.id == review_id).first()
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     return ReviewDetail(
#         id=review.id,
#         user_id=review.user_id,
#         review_type=review.review_type,
#         target_id=review.target_id,
#         rating=review.rating,
#         content=review.content,
#         status=review.status,
#         created_at=review.created_at,
#         updated_at=review.updated_at,
#         extra=review.extra
#     )
# @review_router.put("/reviews/{review_id}", response_model=StatusResponse)
# def update_review(review_id: str, review_data: ReviewUpdate, db: Session = Depends(get_db)):
#     review = db.query(Review).filter(Review.id == review_id).first()
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     if review_data.rating is not None:
#         review.rating = review_data.rating
#     if review_data.content is not None:
#         review.content = review_data.content
#     if review_data.status is not None:
#         review.status = review_data.status
#     if review_data.extra is not None:
#         review.extra = review_data.extra
#     review.updated_at = datetime.utcnow()
#     db.commit()
#     return StatusResponse(status="Review updated successfully")

# @review_router.delete("/reviews/{review_id}", response_model=StatusResponse)
# def delete_review(review_id: str, db: Session = Depends(get_db)):
#     review = db.query(Review).filter(Review.id == review_id).first()
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     db.delete(review)
#     db.commit()
#     return StatusResponse(status="Review deleted successfully")
# @review_router.get("/reviews/user/{user_id}", response_model=List[ReviewDetail])
# def get_reviews_by_user(user_id: str, db: Session = Depends(get_db)):
#     reviews = db.query(Review).filter(Review.user_id == user_id).all()
#     if not reviews:
#         raise HTTPException(status_code=404, detail="No reviews found for the user")
#     return [
#         ReviewDetail(
#             id=review.id,
#             user_id=review.user_id,
#             review_type=review.review_type,
#             target_id=review.target_id,
#             rating=review.rating,
#             content=review.content,
#             status=review.status,
#             created_at=review.created_at,
#             updated_at=review.updated_at,
#             extra=review.extra
#         ) for review in reviews
#     ]
# @review_router.get("/reviews/target/{target_id}", response_model=List[ReviewDetail])
# def get_reviews_by_target(target_id: str, db: Session = Depends(get_db)):
#     reviews = db.query(Review).filter(Review.target_id == target_id).all()
#     if not reviews:
#         raise HTTPException(status_code=404, detail="No reviews found for the target")
#     return [
#         ReviewDetail(
#             id=review.id,
#             user_id=review.user_id,
#             review_type=review.review_type,
#             target_id=review.target_id,
#             rating=review.rating,
#             content=review.content,
#             status=review.status,
#             created_at=review.created_at,
#             updated_at=review.updated_at,
#             extra=review.extra
#         ) for review in reviews
#     ]
# class UpdateReviewStatusRequest(BaseModel):
#     review_id: str
#     status: ReviewStatus

# @review_router.post("/reviews/update_status", response_model=StatusResponse)
# def update_review_status(review_data: UpdateReviewStatusRequest, db: Session = Depends(get_db)):
#     review = db.query(Review).filter(Review.id == review_data.review_id).first()
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     review.status = review_data.status.value
#     review.updated_at = datetime.utcnow()
#     db.commit()
#     return StatusResponse(status="Review status updated successfully")
# @review_router.get("/reviews", response_model=List[ReviewDetail])
# def get_all_reviews(db: Session = Depends(get_db)):
#     reviews = db.query(Review).all()
#     return [
#         ReviewDetail(
#             id=review.id,
#             user_id=review.user_id,
#             review_type=review.review_type,
#             target_id=review.target_id,
#             rating=review.rating,
#             content=review.content,
#             status=review.status,
#             created_at=review.created_at,
#             updated_at=review.updated_at,
#             extra=review.extra
#         ) for review in reviews
#     ]
# class ReviewSearchRequest(BaseModel):
#     user_id: Optional[str]
#     target_id: Optional[str]
#     review_type: Optional[str]
#     status: Optional[str]

# @review_router.post("/reviews/search", response_model=List[ReviewDetail])
# def search_reviews(search_data: ReviewSearchRequest, db: Session = Depends(get_db)):
#     query = db.query(Review)
#     if search_data.user_id:
#         query = query.filter(Review.user_id == search_data.user_id)
#     if search_data.target_id:
#         query = query.filter(Review.target_id == search_data.target_id)
#     if search_data.review_type:
#         query = query.filter(Review.review_type == search_data.review_type)
#     if search_data.status:
#         query = query.filter(Review.status == search_data.status)
#     reviews = query.all()
#     if not reviews:
#         raise HTTPException(status_code=404, detail="No reviews found matching the criteria")
#     return [
#         ReviewDetail(
#             id=review.id,
#             user_id=review.user_id,
#             review_type=review.review_type,
#             target_id=review.target_id,
#             rating=review.rating,
#             content=review.content,
#             status=review.status,
#             created_at=review.created_at,
#             updated_at=review.updated_at,
#             extra=review.extra
#         ) for review in reviews
#     ]


import strawberry
from datetime import datetime
from typing import Optional, List
from dataclasses import field
from sqlalchemy.orm import Session
from app.models.review import Review
from app.database import get_db
import enum
import json

# Enums
@strawberry.enum
class ReviewStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

@strawberry.enum
class ReviewType(enum.Enum):
    PRODUCT = "product"
    STORE = "store"
    SERVICE = "service"

# Types and Inputs
@strawberry.type
class ReviewDetail:
    id: str
    user_id: str
    review_type: ReviewType
    target_id: str
    rating: int
    content: str
    status: ReviewStatus
    created_at: datetime
    updated_at: datetime
    extra: Optional[str]  # Store as JSON string

@strawberry.type
class ReviewResponse:
    message: str
    review_id: str

@strawberry.input
class ReviewCreateInput:
    user_id: str
    review_type: ReviewType
    target_id: str
    rating: int
    content: Optional[str] = ""
    status: Optional[ReviewStatus] = ReviewStatus.PENDING
    extra: Optional[str] = None  # Accept JSON string

@strawberry.input
class ReviewUpdateInput:
    rating: Optional[int]
    content: Optional[str]
    status: Optional[ReviewStatus]
    extra: Optional[str]  # Accept JSON string

# Queries
@strawberry.type
class Query:
    @strawberry.field
    def get_review(self, review_id: str) -> ReviewDetail:
        with get_db() as db:
            review = db.query(Review).filter(Review.id == review_id).first()
            if not review:
                raise Exception("Review not found")
            return ReviewDetail(
                id=review.id,
                user_id=review.user_id,
                review_type=ReviewType(review.review_type),
                target_id=review.target_id,
                rating=review.rating,
                content=review.content,
                status=ReviewStatus(review.status),
                created_at=review.created_at,
                updated_at=review.updated_at,
                extra=review.extra
            )

    @strawberry.field
    def get_reviews_by_user(self, user_id: str) -> List[ReviewDetail]:
        with get_db() as db:
            reviews = db.query(Review).filter(Review.user_id == user_id).all()
            if not reviews:
                raise Exception("No reviews found for the user")
            return [
                ReviewDetail(
                    id=review.id,
                    user_id=review.user_id,
                    review_type=ReviewType(review.review_type),
                    target_id=review.target_id,
                    rating=review.rating,
                    content=review.content,
                    status=ReviewStatus(review.status),
                    created_at=review.created_at,
                    updated_at=review.updated_at,
                    extra=json.dumps(review.extra) if review.extra else None
                ) for review in reviews
            ]

# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_review(self, review_data: ReviewCreateInput) -> ReviewResponse:
        with get_db() as db:
            new_review = Review(
                user_id=review_data.user_id,
                review_type=review_data.review_type.value,
                target_id=review_data.target_id,
                rating=review_data.rating,
                content=review_data.content,
                status=review_data.status.value,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                extra=json.loads(review_data.extra) if review_data.extra else {}
            )
            db.add(new_review)
            db.commit()
            db.refresh(new_review)
            return ReviewResponse(message="Review created successfully", review_id=new_review.id)

    @strawberry.mutation
    def update_review(self, review_id: str, review_data: ReviewUpdateInput) -> str:
        with get_db() as db:
            review = db.query(Review).filter(Review.id == review_id).first()
            if not review:
                raise Exception("Review not found")
            if review_data.rating is not None:
                review.rating = review_data.rating
            if review_data.content is not None:
                review.content = review_data.content
            if review_data.status is not None:
                review.status = review_data.status.value
            if review_data.extra is not None:
                review.extra = json.loads(review_data.extra)
            review.updated_at = datetime.utcnow()
            db.commit()
            return "Review updated successfully"

    @strawberry.mutation
    def delete_review(self, review_id: str) -> str:
        with get_db() as db:
            review = db.query(Review).filter(Review.id == review_id).first()
            if not review:
                raise Exception("Review not found")
            db.delete(review)
            db.commit()
            return "Review deleted successfully"

# Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
