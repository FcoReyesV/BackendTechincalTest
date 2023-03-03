class Admin:
    def __init__(self, admin_id: str, username: str, email: str, password: str):
        self.admin_id = admin_id
        self.username = username
        self.email = email
        self.password = password
    
    @classmethod
    def from_dict(cls, admin_dict: dict) -> "Admin":
        return cls(admin_dict["_id"], admin_dict["username"], admin_dict["email"], admin_dict["password"])
        