from app import app
from app.models.user import User


class LoginService:

    @staticmethod
    def loginUser(username: str, password_hash: str) -> str:
        """This method is used to check if user is present in database or not

        Args:
            username (str): username
            password_hash (str): hash of password

        Raises:
            Exception: exception is raised if cannot query the database

        Returns:
            str: client id(if user is authenticated), None(if user is not authenticated)
        """

        try:
            user = User.query.filter_by(
                username=username, password_hash=password_hash).first()
        except Exception as e: 
            app.logger.error(e)
            raise Exception("database error") from None

        if user is None:
            return None

        return user.client_id
