"""数据库连接配置：db/base.py"""
import os
import string
import secrets
import app.models.table_model as models
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('POSTGRES_URL')
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables_if_not_exist():
    models.Base.metadata.create_all(bind=engine, checkfirst=True)
    create_admin_if_not_exists()


def create_admin_if_not_exists():
    from app.models.user_model import RegisterUser
    from app.services.user_service import register_new_user
    admin_username = 'admin'
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        admin_password = ''.join(secrets.choice(alphabet) for _ in range(8))
        if (any(c.isupper() for c in admin_password)
                and any(c.islower() for c in admin_password)
                and any(c.isdigit() for c in admin_password)
                and any(not c.isalnum() for c in admin_password)):
            break
    admin = RegisterUser(
        username=admin_username,
        email='admin@dbcd.oky.wiki',
        password=admin_password,
        hashed_password='',
        is_admin=True,
        is_disabled=False
    )
    register_new_user(admin)
    print(f"Generated Admin Username: {admin_username}")
    print(f"Generated Admin Password: {admin_password}")


def tables_exist():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    expected_tables = models.Base.metadata.tables.keys()
    return all(table in existing_tables for table in expected_tables)


def admin_exist():
    from app.db.crud.user_crud import get_user
    admin_username = 'admin'
    admin = get_user(admin_username)
    return admin is not None
