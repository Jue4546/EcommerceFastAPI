"""数据库连接配置：db/base.py"""
import os
import psycopg2
import psycopg2.extensions

DATABASE_URL = os.getenv('POSTGRES_URL', 'postgres://default:BlkLu4Efzr3a@ep-broken-mode-99984904-pooler.us-east-1'
                                         '.postgres.vercel-storage.com/verceldb')


def get_db_connection():
    db_config = psycopg2.extensions.make_dsn(DATABASE_URL)
    return psycopg2.connect(db_config)

