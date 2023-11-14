from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def all(self) -> List[User]:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        pass
