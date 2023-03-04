import abc
from typing import Optional
from admin.domain.admin_model import Admin

class ISuperAdminRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, new_admin: Admin) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_by_id(self, field: str, key: str) -> Optional[Admin]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_all(self) -> list[Admin]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update(self, admin_to_update: Admin) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, field: str, key: str) -> bool:
        raise NotImplementedError
    
class AdminRepositoryException(Exception):
    pass
