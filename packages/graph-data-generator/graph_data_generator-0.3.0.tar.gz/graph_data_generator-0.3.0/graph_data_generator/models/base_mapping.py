import abc
from dataclasses import dataclass

@dataclass
class BaseMapping(abc.ABC):
    # Parent abstract class for NodeMapping, RelationshipMapping, and PropertyMapping objects.

    @staticmethod
    @abc.abstractmethod
    def empty():
        pass

    @abc.abstractclassmethod
    def to_dict(self) -> dict:
        pass

    @abc.abstractmethod
    def filename(self) -> str:
        pass

    @abc.abstractmethod
    def ready_to_generate(self) -> bool:
        pass

    # TODO: callable signature needs a return type
    @abc.abstractmethod
    def generate_values(self)-> list[dict]:
        """
        Generates new data for the mapping.
        
        Returns:
            A list of dictionary data where each dictionary is a record of the generated data.  
        """
        pass

    @abc.abstractmethod
    def generated_values(self) -> list[dict]:
        """
        Retrieves previously generated data. If no data was previously generated, will create new data before returning.
        
        Returns:
            A list of dictionary data where each dictionary is a record of the generated data.
        """
        pass