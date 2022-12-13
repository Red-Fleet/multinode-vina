from app import db, app
from app.models.user import User
from sqlalchemy.exc import IntegrityError

class RegisterService:
    @staticmethod
    def registerUser(username:str, password_hash:str) -> str:
        if username == "":
            raise Exception("username cannot be null")
        user = User(username=username, password_hash=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            raise Exception("username taken") 
        except Exception as e:
            app.logger.error(e)
            raise Exception("database error")

        return user.client_id