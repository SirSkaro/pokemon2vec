from abc import ABC, abstractmethod
from typing import List


class TeamFactory(ABC):

    @abstractmethod
    def get_teams(self) -> List[List[str]]:
        pass

