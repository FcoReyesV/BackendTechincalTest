import abc
from product.domain import admin

class ISuperAdminRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_admin(self, id_admin: str) -> admin.Admin:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_all_admins(self) -> list[admin.Admin]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def create_admin(self, new_admin: admin.Admin) -> admin.Admin:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_admin(self, admin: admin.Admin) -> admin.Admin:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_admin(self, id_admin: str) -> None:
        raise NotImplementedError
