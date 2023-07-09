class User:
    def __init__(self) -> None:
        self.username: str = None
        self.password: str = None
        self.client_id: str = None
        self.isAuthenticated: bool = False
        self.name: str = None

        self.username: str = "user1"
        self.password: str = "pass"
        self.client_id: str = "client_id"
        self.isAuthenticated: bool = True
        self.name: str = "user 1"