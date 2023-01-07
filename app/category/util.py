from app import db
from app.models import Category
from slugify import slugify


def fill_existing_categories_slug():
    for category in db.session.query(Category):
        if not category.slug:
            category.slug = slugify(category.category)
    
    db.session.commit()