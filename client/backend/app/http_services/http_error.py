class HttpError:
    @staticmethod
    def isHttpError(status_code: int)->bool:
        if status_code<200 or status_code>299:
            return True
        return False