import os
from O365 import Account
from app.db.crud.mail_crud import PostgresBackend
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('MICROSOFT_CLIENT_ID')
client_secret = os.getenv('MICROSOFT_CLIENT_SECRET')
credentials = (client_id, client_secret)


# 使用你的凭据创建 Account 对象
scopes = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send']
account = Account(credentials, token_backend=PostgresBackend(), scopes=scopes)


def send_verification_email(email_address: str, verification_code: str):
    # 创建邮件内容
    m = account.new_message()
    m.to.add(email_address)
    m.subject = 'Verification Code'
    m.body = f'Your verification code is: {verification_code}'
    m.send()
    return True
