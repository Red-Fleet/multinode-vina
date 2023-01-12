class User:
    def __init__(self) -> None:
        self.username: str = None
        self.password: str = None
        self.client_id: str = None
        self.isAuthenticated: bool = False
        self.name: str = None