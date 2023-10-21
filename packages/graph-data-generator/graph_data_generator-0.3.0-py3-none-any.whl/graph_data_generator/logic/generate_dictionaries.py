
from graph_data_generator.models.mapping import Mapping
from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.logger import ModuleLogger


def generate_dictionaries(mapping: Mapping) -> dict:
    """Generates a dictionary of nodes and relationships records. Uses a mapping process to generate mock data.

    Args:
        mapping: A master Mapping object containing node and relationship mappings.
    
    Returns:
        A dictionary with 'nodes' and 'relationships' keys containing lists of dictionaries of generated records as dictionaries.
    """

    # A no node scenarios it not possible to generate any data
    if len(mapping.nodes) == 0:
        raise Exception(f'No nodes found in mapping. Cannot generate data.')

    output = {"nodes":{}, "relationships":{}}

    for nodeMapping in mapping.nodes.values():
        values : list[dict] = nodeMapping.generated_values()
        key = f'{nodeMapping.caption}'
        output['nodes'][key] = values
    
    for relMapping in mapping.relationships.values():
        values : list[dict] = relMapping.generated_values()
        key = f'{relMapping.type}'
        output['relationships'][key] = values

    return output