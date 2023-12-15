"""数据库连接配置：db/base.py"""
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()
DATABASE_URL = os.getenv('POSTGRES_URL')


def get_db_connection():
    return psycopg.connect(DATABASE_URL)
