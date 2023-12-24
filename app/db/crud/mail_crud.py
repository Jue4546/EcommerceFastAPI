from O365.utils.token import BaseTokenBackend, log

from app.db.base import SessionLocal
from app.models.table_model import Token as TokenModel


class PostgresBackend(BaseTokenBackend):
    def __init__(self):
        super().__init__()

    def load_token(self):
        """
        Retrieves the token from the database
        :return dict or None: The token if exists, None otherwise
        """
        token = None
        try:
            db = SessionLocal()
            token_data = db.query(TokenModel).first()
            db.close()

            if token_data:
                # Convert data from the database to a Token object
                token = self.token_constructor({
                    'access_token': token_data.access_token,
                    'refresh_token': token_data.refresh_token,
                    'expires_at': token_data.expires_at,
                    'is_expired': token_data.is_expired
                    # Add other fields as needed
                })
        except Exception as e:
            log.error("Token could not be retrieved from the backend: {}".format(e))

        return token

    def save_token(self):
        """
        Saves the token dict in the database
        :return bool: Success / Failure
        """
        if self.token is None:
            raise ValueError('You have to set the "token" first.')

        try:
            db = SessionLocal()
            token_model = TokenModel(
                access_token=self.token.get('access_token'),
                refresh_token=self.token.get('refresh_token'),
                expires_at=self.token.get('expires_at'),
                is_expired=self.token.get('is_expired')
            )
            db.add(token_model)
            db.commit()
            db.close()
        except Exception as e:
            log.error("Token could not be saved: {}".format(e))
            return False

        return True
