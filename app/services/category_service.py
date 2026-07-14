from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)


class CategoryService:
    @staticmethod
    def get_all_categories(db: Session):
        return db.query(Category).order_by(Category.name).all()

    @staticmethod
    def get_category(db: Session, category_id):
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def create_category(
        db: Session,
        category_data: CreateCategoryRequest,
    ):
        category = Category(**category_data.model_dump())

        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def update_category(
        db: Session,
        category: Category,
        category_data: UpdateCategoryRequest,
    ):
        update_data = category_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(category, field, value)

        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def delete_category(
        db: Session,
        category: Category,
    ):
        db.delete(category)
        db.commit()