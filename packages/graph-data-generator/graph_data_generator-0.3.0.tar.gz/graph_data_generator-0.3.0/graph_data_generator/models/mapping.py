
from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.relationship_mapping import RelationshipMapping
from graph_data_generator.logger import ModuleLogger
import json
import sys


class Mapping():
    # For storing all mapping data. Stores lists of NodeMapping and RelationshipMapping objects.

    @staticmethod
    def empty():
        return Mapping({}, {})
        
    def __init__(self, nodes : dict[str, NodeMapping] = {}, relationships : dict[str, RelationshipMapping] = {}):
        self.nodes = nodes
        self.relationships = relationships
        self._did_generate_values = False

    def __str__(self):
        return f"'Mapping':{{'nodes': {self.nodes}, 'relationships': {self.relationships} }})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "mapping" :{
                "nodes": {key: value.to_dict() for key, value in self.nodes.items()},
                "relationships": {key: value.to_dict() for key, value in self.relationships.items()}
            }
        }

    def is_empty(self):
        if len(self.nodes) > 0:
            return False
        if len(self.relationships) > 0:
            return False
        return True

    def is_valid(self):
        # TODO: Actually validate data content

        for node in self.nodes.values():
            if node.ready_to_generate() == False:
                return False
        for relationship in self.relationships.values():
            if relationship.ready_to_generate() == False:
                return False

        try:
            json.loads(json.dumps(self.to_dict()))
            return True
        except ValueError as err:
            ModuleLogger().error(f'mapping.py (model): is_valid. ERROR: {err} for mapping: {self}')
            return False
        except:
            ModuleLogger().error(f'mapping.py (model): is_valid. ERROR: {sys.exc_info()[0]} for mapping: {self}')
            return False
        
    def did_generate_values(self):
        return self._did_generate_values
    
    def _request_nodes(self, node_caption: str) -> list[NodeMapping]:
        return [node for node in self.nodes.values() if node.caption == node_caption]
    
    def _request_relationships(self, relationship_type: str) -> list[RelationshipMapping]:
        return [rel for rel in self.relationships.values() if rel.type == relationship_type]

    def _request_elements(self, name: str) -> list[BaseMapping]:
        # Returns all nodes and relationship mapping objects with caption or type name
        nodes = self._request_nodes(name)
        relationships = self._request_relationships(name)
        return nodes + relationships
    
    def generate_values(self):
        for nodeMappings in self.nodes.values():
            nodeMappings.generate_values()
        for relMappings in self.relationships.values():
            relMappings.generate_values()
        self._did_generate_values = True
